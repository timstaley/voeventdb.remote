"""
Helper classes for providing convenience parsing of returned JSON content.
"""
from astropy.coordinates import SkyCoord, Angle
from astropy.time import Time
import iso8601
import logging
from copy import deepcopy

logging.getLogger('iso8601').setLevel(logging.INFO)
import pprint


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
        self.position= SkyCoord(d['ra'], d['dec'], unit='deg')
        self.position_error = Angle(d['error'], unit='deg')
        self.timestamp = iso8601.parse_date(d['time'])

    def __repr__(self):
        return (str(self.position)
                +' +/- ' + self.position_error.to_string(decimal=True)
               +' @ ' + self.timestamp.isoformat())

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
        author_ivorn (string): The ``Who.AuthorIVORN`` entry. May be
            None if no entry present in the VOEvent packet.
        ivorn (string)
        received (:class:`datetime.datetime`): Dates exactly when the packet
            was loaded into this instance of voeventdb.
        role (string)
        stream (string)
        version (string)
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
    def __init__(self, synopsis_dict, api_version_string='apiv0'):


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
        display_vars=deepcopy(display_vars)
        display_vars.pop('coords')
        for k, v in display_vars.items():
            if hasattr(v, 'isoformat'):
                display_vars[k] = v.isoformat()

        pp = pprint.PrettyPrinter(indent=2)
        return pp.pformat(display_vars)


