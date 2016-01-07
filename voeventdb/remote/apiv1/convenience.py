"""
Convenience functions for exploring / extracting more complex data-structures.
"""
from voeventdb.remote.helpers import _map_citations
from voeventdb.remote.apiv1.endpoints import packet_synopsis, list_ivorn
from voeventdb.remote.apiv1.definitions import FilterKeys

def _fetch_refs(ivorn):
    return [r['ref_ivorn'] for r in packet_synopsis(ivorn)['refs']]

def _fetch_cites(ref_ivorn):
    return list_ivorn({FilterKeys.ref_exact : ref_ivorn})

def citation_network_map(ivorn, max_recursion_levels=5):
    defaultdict_map =  _map_citations(
        ivorn=ivorn,
        fetch_refs_func=_fetch_refs,
        fetch_citations_func=_fetch_cites,
        max_recursion=max_recursion_levels
    )
    return dict(defaultdict_map)