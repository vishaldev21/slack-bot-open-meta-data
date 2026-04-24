from ..metadata_changes.request import get_data

def get_impact_wrapper(result):
    if type(result) is str:
        return result
    strResult = ""
    for item in result:
        strResult += f"name: {item["name"]} fqn: {item["fqn"]} serviceType: {item["serviceType"]}\n"
    return strResult

def get_impact(entity, fqn: str) -> list|str:
    """
    Fetch downstream lineage for a table and return affected systems in Slack format.
    """
    lineage_entity = entity[0:len(entity)-1]
    url = f"lineage/{lineage_entity}/name/{fqn}?downstreamDepth=3"
    data, err = get_data(url)
    if err is not None:
        return "Failed to fetch entity details"
    if data is None:
        return "Failed to fetch entity details"
    
    downstream = data.get("downstreamEdges")
    affected = []
    if len(downstream) <= 0:
        return "No Downstream found"
    
    for edge in downstream:
        node = edge.get("toEntity")
        affected.append(node)

    result = []
    for items in affected:
        entity_url = f"{entity}/{items}"
        entity_data, error =  get_data(entity_url)
        if error is not None:
            return "Failed to fetch entity details"
        if entity_data is None:
            result.append(None)
        name = entity_data.get("name")
        fqn = entity_data.get("fullyQualifiedName")
        serviceType = entity_data.get("serviceType")
        result.append({"name":name,"fqn":fqn,"serviceType":serviceType})
    return result

