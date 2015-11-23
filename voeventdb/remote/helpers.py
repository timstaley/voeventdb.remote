"""
Helper classes for providing convenience parsing of returned JSON content.
"""
from astropy.coordinates import SkyCoord
from astropy.time import Time
import iso8601
import logging
from copy import deepcopy

logging.getLogger('iso8601').setLevel(logging.INFO)
import pprint


class CoordsWithTimestamp(object):
    def __init__(self, sky_position, time):
        self.coords = sky_position
        self.timestamp = time
    def __repr__(self):
        return str(self.coords)+' @ '+self.timestamp.isoformat()

class Synopsis(object):
    def __init__(self, synopsis_dict, api_version_string='apiv0'):
        self._synopsis_dict = synopsis_dict.copy()

        self.coords_with_timestamp = [self._parse_coords_dict(d)
                        for d in synopsis_dict['coords']]

        self.coords = [e.coords for e in self.coords_with_timestamp]

        self.references = self._synopsis_dict['refs']

        voevent_dict = synopsis_dict['voevent']
        self.author_datetime = iso8601.parse_date(
            voevent_dict['author_datetime'])
        self.author_ivorn = voevent_dict['author_ivorn']
        self.ivorn = voevent_dict['ivorn']
        self.received = iso8601.parse_date(
            voevent_dict['received'])
        self.role = voevent_dict['role']
        self.stream = voevent_dict['stream']
        self.version = voevent_dict['version']

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

    @staticmethod
    def _parse_coords_dict(coords_dict):
        d = coords_dict
        posn = SkyCoord(d['ra'], d['dec'], unit='deg')
        time = iso8601.parse_date(d['time'])
        return CoordsWithTimestamp(posn,time)
