import networkx as nx

from parser import (
    extract_router_id,
    extract_summary_lsas,
    extract_router_nodes,
    extract_router_links,
    extract_prefix_advertisements
)


def analyze_prefix(lsdb_text, target_prefix):

    # Router where LSDB was captured
    router_id = extract_router_id(lsdb_text)

    # Detect prefix advertisements + LSA type
    prefix_ads = extract_prefix_advertisements(lsdb_text, target_prefix)

    advertisements = []
    lsa_type = None

    for entry in prefix_ads:
        advertisements.append(entry["advertising_router"])
        lsa_type = entry["lsa_type"]

    # Extract router nodes
    routers = extract_router_nodes(lsdb_text)

    # Build topology graph
    G = nx.Graph()

    for r in routers:
        G.add_node(r)

    # Extract router links
    links = extract_router_links(lsdb_text)

    for a, b, metric in links:
        G.add_edge(a, b, weight=metric)

    # Compute SPF paths
    paths = []

    for r in advertisements:

        try:

            path = nx.shortest_path(G, router_id, r, weight="weight")
            cost = nx.shortest_path_length(G, router_id, r, weight="weight")
            hops = len(path) - 1

        except nx.NetworkXNoPath:

            path = None
            cost = None
            hops = None

        paths.append({
            "router": r,
            "cost": cost,
            "hops": hops,
            "path": path
        })

    # Sort by SPF cost
    # paths = sorted(
    #     paths,
    #     key=lambda x: (x["cost"] if x["cost"] is not None else 999999)
    # )
    #paths.sort(key=lambda x: x.get("cost") if x.get("cost") is not None else 999999)

    def safe_cost(entry):
        cost = entry.get("cost")
        if isinstance(cost, (int, float)):
            return cost
        return 999999


    paths = sorted(paths, key=safe_cost)

    return {
        "source_router": router_id,
        "prefix": target_prefix,
        "lsa_type": lsa_type,
        "occurrences": len(advertisements),
        "paths": paths
    }


if __name__ == "__main__":

    with open("sample_lsdb.txt") as f:
        data = f.read()

    prefix = "10.199.246.8"

    result = analyze_prefix(data, prefix)

    print("\nOSPF PREFIX ANALYSIS")
    print("--------------------")

    print("Source Router :", result["source_router"])
    print("Prefix        :", result["prefix"])
    print("Type          :", result["lsa_type"])
    print("Advertisements:", result["occurrences"])

    # Handle prefix not found
    if not result["paths"]:

        print("\nNo advertisement found for this prefix in LSDB.")
        exit()

    print("\nBest Path Candidate")

    best = result["paths"][0]

    print("Router :", best["router"])
    print("Cost   :", best["cost"])
    print("Hops   :", best["hops"])

    print("\nBest Path")

    if best["path"]:
        print(" -> ".join(best["path"]))

    print("\nAll Advertising Routers (sorted by SPF cost)\n")

    for entry in result["paths"]:

        print(
            entry["router"],
            " cost:", entry["cost"],
            " hops:", entry["hops"]
        )

        if entry["path"]:
            print("   path:", " -> ".join(entry["path"]))