"""
Helper classes for providing convenience parsing of returned JSON content.
"""
import logging
import pprint
from collections import defaultdict
from copy import deepcopy

import iso8601
from astropy.coordinates import Angle, SkyCoord
from astropy.time import Time

logging.getLogger('iso8601').setLevel(logging.INFO)

logger = logging.getLogger(__name__)


class SkyEvent(object):
    """
    Represents universal attributes of an observed event on sky.

    I.e. the most basic details that we expect to find in all packets
    reporting events with sky-positions.

    Attributes:
        position (:class:`astropy.coordinates.SkyCoord`): Best-estimate
            sky-coordinates of the event being reported.

        position error (:class:`astropy.coordinates.Angle`): Error-cone on the
            position estimate.

        timestamp of event (:class:`datetime.datetime`):
            Timestamp for the reported event (UTC timezone).

    """

    def __init__(self, skyevent_dict):
        d = skyevent_dict
        self.position = SkyCoord(d['ra'], d['dec'], unit='deg')
        self.position_error = Angle(d['error'], unit='deg')
        self.timestamp = None
        if d.get('time'):
            self.timestamp = iso8601.parse_date(d['time'])

    def __repr__(self):
        return (str(self.position)
                + ' +/- ' + self.position_error.to_string(decimal=True)
                + ' @ ' + self.timestamp.isoformat())

    @staticmethod
    def _parse_coords_dict(coords_dict):
        d = coords_dict
        posn = SkyCoord(d['ra'], d['dec'], unit='deg')
        posn_error = Angle(d['error'], unit='deg')
        time = iso8601.parse_date(d['time'])
        return SkyEvent(sky_position=posn,
                        sky_position_error=posn_error,
                        event_timestamp=time)


class Synopsis(object):
    """
    Parses the output from the 'synopsis' endpoint into a class-object.

    Attributes:
        author_datetime (:class:`datetime.datetime`): The ``Who.Date`` timestamp.
            (Parsed to datetime, UTC timezone). May be ``None`` if no timestamp
            present in the VOEvent packet.
        author_ivorn (str): The ``Who.AuthorIVORN`` entry. May be
            None if no entry present in the VOEvent packet.
        ivorn (str)
        received (:class:`datetime.datetime`): Dates exactly when the packet
            was loaded into this instance of voeventdb.
        role (str)
        stream (str)
        version (str)
        sky_events (list): A list of :class:`SkyEvent` objects.
            These are parsed from the `WhereWhen` section of a VOEvent
            packet, if possible. (If the packet has no WhereWhen data,
            this is an empty list).
        coords (list): :class:`astropy.coordinates.SkyCoord` positions.
            This is a syntax-shortcut, the positions are just those of the
            :attr:`.sky_events` entries, if any are present.
        references (list): References to other VOEvent packets.
            This is a list of dictionaries representing any references
            present in the ``Citations`` section of the VOEvent packet.

    """

    def __init__(self, synopsis_dict, api_version_string='apiv1'):

        voevent_dict = synopsis_dict['voevent']

        self.author_datetime = None
        if voevent_dict['author_datetime']:
            self.author_datetime = iso8601.parse_date(
                voevent_dict['author_datetime'])

        self.author_ivorn = None
        if voevent_dict['author_ivorn']:
            self.author_ivorn = voevent_dict['author_ivorn']

        self.ivorn = voevent_dict['ivorn']
        self.received = iso8601.parse_date(
            voevent_dict['received'])
        self.role = voevent_dict['role']
        self.stream = voevent_dict['stream']
        self.version = voevent_dict['version']

        self._synopsis_dict = synopsis_dict.copy()

        self.sky_events = [SkyEvent(d) for d in synopsis_dict['coords']]

        self.coords = [e.position for e in self.sky_events]

        self.references = self._synopsis_dict['refs']

    def __repr__(self):
        # Can be pasted back in to recreate the object
        return "Synopsis({})".format(self._synopsis_dict)

    def __str__(self):
        # Bit hacky, probably overkill:
        display_vars = {k: v for k, v in vars(self).items()
                        if not k.startswith('_')}
        display_vars = deepcopy(display_vars)
        display_vars.pop('coords')
        for k, v in display_vars.items():
            if hasattr(v, 'isoformat'):
                display_vars[k] = v.isoformat()

        pp = pprint.PrettyPrinter(indent=2)
        return pp.pformat(display_vars)


def _map_citations(ivorn,
                   fetch_refs_func,
                   fetch_citations_func,
                   cite_map=None,
                   previously_mapped=None,
                   prev_recursion_level=None,
                   max_recursion=None,
                   ):
    """
    Perform a depth first search on the citation-network.

    (API agnostic version, should be wrapped for convenience)

    Stop at max_recursion links from initial node / IVORN.

    Returns:
        citation_map (dict): A dictionary containing all the VOEvents in this
            network, to max_recursion level specified.
            The dictionary maps an 'origin' IVORN to its citing packets,
            i.e.::

                { origin_ivorn : {citing_ivorn1, ..., citing_ivornN} }

            We could have inverted the relationship (map packet_ivorn->included references)
            but since the typical behaviour is for many packets to cite one origin
            packet, this usually results in a more compact representation.

    """

    if prev_recursion_level is None:
        current_recursion_level = 0
    else:
        current_recursion_level = prev_recursion_level + 1
    logger.debug('Fetching for {}, at recursion level {}'.format(
        ivorn, current_recursion_level))

    if cite_map is None:
        cite_map = defaultdict(set)
    if previously_mapped is None:
        previously_mapped = set()
    logger.debug('{} packets mapped'.format(len(previously_mapped)))
    ref_ivorns = fetch_refs_func(ivorn)
    for ri in ref_ivorns:
        # Add a 'citation' entry to the cite_map of the origin-ivorn being referenced.
        cite_map[ri].add(ivorn)
    citing_ivorns = fetch_citations_func(ivorn)
    for ci in citing_ivorns:
        cite_map[ivorn].add(ci)
    previously_mapped.add(ivorn)
    if not max_recursion or (current_recursion_level < max_recursion):
        for ri in ref_ivorns:
            if ri not in previously_mapped:
                cite_map.update(_map_citations(
                    ivorn=ri,
                    fetch_refs_func=fetch_refs_func,
                    fetch_citations_func=fetch_citations_func,
                    cite_map=cite_map,
                    previously_mapped=previously_mapped,
                    prev_recursion_level=current_recursion_level,
                    max_recursion=max_recursion,
                ))
        for ci in citing_ivorns:
            if ci not in previously_mapped:
                cite_map.update(_map_citations(
                    ivorn=ci,
                    fetch_refs_func=fetch_refs_func,
                    fetch_citations_func=fetch_citations_func,
                    cite_map=cite_map,
                    previously_mapped=previously_mapped,
                    prev_recursion_level=current_recursion_level,
                    max_recursion=max_recursion,
                ))
    return cite_map
