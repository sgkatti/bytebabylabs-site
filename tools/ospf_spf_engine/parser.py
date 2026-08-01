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

def extract_prefix_advertisements(text, target_prefix):

    entries = []
    current_lsa = None
    advertising_router = None

    for line in text.splitlines():

        if "LS Type:" in line:

            if "router-LSA" in line:
                current_lsa = "Type-1"

            elif "summary-LSA" in line:
                current_lsa = "Type-3"

            elif "AS-external-LSA" in line or "AS External" in line:
                current_lsa = "Type-5"

        if "Advertising Router:" in line:
            advertising_router = line.split(":")[1].strip()

        if target_prefix in line:

            entries.append({
                "prefix": target_prefix,
                "lsa_type": current_lsa,
                "advertising_router": advertising_router
            })

    return entries

def detect_prefix_type(text, prefix):

    if "Type-5" in text or "AS External Link States" in text:
        if prefix in text:
            return "Type-5"

    if "Summary Net Link States" in text:
        if prefix in text:
            return "Type-3"

    if "Router Link States" in text:
        if prefix in text:
            return "Type-1"

    return "Unknown"