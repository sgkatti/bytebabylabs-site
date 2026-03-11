import re

def extract_router_id(text):

    match = re.search(r"OSPF Router with ID \((.*?)\)", text)

    if match:
        return match.group(1)

    return None


def extract_summary_lsas(text):

    results = []

    lines = text.splitlines()

    for line in lines:

        if "/" in line:

            parts = line.split()

            if len(parts) >= 6:

                prefix = parts[-1]
                adv_router = parts[1]

                results.append({
                    "prefix": prefix,
                    "advertising_router": adv_router
                })

    return results

def extract_router_nodes(text):

    routers = []

    lines = text.splitlines()

    for line in lines:

        if re.match(r"\d+\.\d+\.\d+\.\d+\s+\d+\.\d+\.\d+\.\d+", line):

            parts = line.split()

            router_id = parts[0]

            routers.append(router_id)

    return routers

def extract_router_links(text):

    import re

    edges = []

    current_router = None
    current_neighbor = None

    lines = text.splitlines()

    for line in lines:

        # detect advertising router
        if "Advertising Router:" in line:
            current_router = line.split(":")[1].strip()

        # detect neighboring router
        if "Neighboring Router ID:" in line:
            current_neighbor = line.split(":")[1].strip()

        # detect metric
        if "Metric:" in line and current_router and current_neighbor:

            metric = int(line.split(":")[1].strip())

            edges.append((current_router, current_neighbor, metric))

            current_neighbor = None

    return edges
