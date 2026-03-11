import re

def analyze_ospf(text, prefix):
    routers = []
    lsa_blocks = text.split("LS age")

    for block in lsa_blocks:
        if prefix in block:

            adv_router = re.search(r"Advertising Router: (\S+)", block)
            lsa_type = re.search(r"LS Type: (\S+)", block)

            routers.append({
            "advertising_router": adv_router.group(1) if adv_router else "unknown",
            "lsa_type": lsa_type.group(1) if lsa_type else "unknown"
            })

    return {
        "prefix": prefix,
        "matches_found": len(routers),
        "advertisements": routers
    }

