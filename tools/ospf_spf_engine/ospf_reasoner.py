import networkx as nx
from parser import extract_router_id, extract_summary_lsas, extract_router_nodes
from parser import extract_router_id, extract_summary_lsas, extract_router_nodes, extract_router_links



def analyze_prefix(lsdb_text, target_prefix):

    # Identify router where LSDB was taken
    router_id = extract_router_id(lsdb_text)

    # Extract prefix advertisements
    summaries = extract_summary_lsas(lsdb_text)

    advertisements = []

    for entry in summaries:

        if target_prefix in entry["prefix"]:
            advertisements.append(entry["advertising_router"])

    # Extract routers from LSDB
    routers = extract_router_nodes(lsdb_text)

    # Build graph
    G = nx.Graph()

    for r in routers:
        G.add_node(r)
        
    links = extract_router_links(lsdb_text)

    for a, b in links:
        G.add_edge(a, b, weight=1)


    # Compute paths from source router to advertising routers
    paths = []

    for r in advertisements:

        try:
            path = nx.shortest_path(G, router_id, r)
        except:
            path = None

        paths.append({
            "router": r,
            "path": path
        })

    return {
        "source_router": router_id,
        "prefix": target_prefix,
        "occurrences": len(advertisements),
        "paths": paths
    }


if __name__ == "__main__":

    with open("sample_lsdb.txt") as f:
        data = f.read()

    result = analyze_prefix(data, "10.199.240.163")

    print(result)
