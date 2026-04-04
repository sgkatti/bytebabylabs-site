import networkx as nx

from parser import (
    extract_router_id,
    extract_router_nodes,
    extract_router_links
)


def detect_advertising_routers(lsdb_text, prefix):
    """
    Detect routers advertising the prefix by scanning LSDB sections.
    Works with router-LSA stub networks and summary LSAs.
    """

    advertisements = []
    current_router = None

    for line in lsdb_text.splitlines():

        line = line.strip()

        if "Advertising Router:" in line:
            current_router = line.split(":")[1].strip()

        if prefix in line:
            if current_router:
                advertisements.append(current_router)

    return list(set(advertisements))


def analyze_prefix(lsdb_text, target_prefix):

    # Identify router where LSDB was taken
    router_id = extract_router_id(lsdb_text)

    # Detect routers advertising prefix
    advertisements = detect_advertising_routers(lsdb_text, target_prefix)

    # Extract router nodes
    routers = extract_router_nodes(lsdb_text)

    # Build topology graph
    G = nx.Graph()

    for r in routers:
        G.add_node(r)

    links = extract_router_links(lsdb_text)

    for a, b, metric in links:
        G.add_edge(a, b, weight=metric)

    # Run SPF from source router
    try:
        distances, spf_paths = nx.single_source_dijkstra(G, router_id, weight="weight")
    except:
        distances = {}
        spf_paths = {}

    paths = []

    for r in advertisements:

        if r in distances:

            cost = distances[r]
            path = spf_paths[r]
            hops = len(path) - 1

            paths.append({
                "router": r,
                "cost": cost,
                "hops": hops,
                "path": path
            })

    # Sort by best SPF cost
    paths.sort(key=lambda x: x["cost"])

    return {
        "source_router": router_id,
        "prefix": target_prefix,
        "occurrences": len(advertisements),
        "paths": paths
    }


if __name__ == "__main__":

    prefix = input("Enter prefix to analyse: ")

    with open("sample_lsdb.txt") as f:
        data = f.read()

    result = analyze_prefix(data, prefix)

    print("\nOSPF PREFIX ANALYSIS")
    print("--------------------")

    print("Source Router :", result["source_router"])
    print("Prefix        :", result["prefix"])
    print("Advertisements:", result["occurrences"])

    if not result["paths"]:
        print("\nNo reachable advertising router found.")
        exit()

    best = result["paths"][0]

    print("\nBest Path Candidate")
    print("Router :", best["router"])
    print("Cost   :", best["cost"])
    print("Hops   :", best["hops"])

    print("\nBest Path")
    print(" -> ".join(best["path"]))

    print("\nReachable Advertising Routers (sorted by SPF cost)\n")

    for entry in result["paths"][:10]:   # limit output to first 10

        print(
            entry["router"],
            " cost:", entry["cost"],
            " hops:", entry["hops"]
        )