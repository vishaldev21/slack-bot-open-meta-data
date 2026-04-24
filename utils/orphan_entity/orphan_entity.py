from ..metadata_changes.request import get_data
import httpx


def get_orphan_entity(entityType, fqn) -> bool | str:
    lineage_url = f"lineage/{entityType}/name/{fqn}?downstreamDepth=3"
    table_data, error = get_data(lineage_url)
    if error is not None:
        return "Error fetching tables"
    if table_data is None:
        return "No data found"
    downstream_edges = table_data.get("downstreamEdges")
    return False if len(downstream_edges) > 0 else True
