#!/usr/bin/env bash
set -e

echo "Creating ByteBabyLabs API structure..."

mkdir -p api
cd api

# requirements

cat << 'EOF' > requirements.txt
fastapi
uvicorn
python-multipart
networkx
EOF

# main.py

cat << 'EOF' > main.py
from fastapi import FastAPI, UploadFile, Form
from ospf_parser import analyze_ospf

app = FastAPI(title="ByteBabyLabs Network Engine")

@app.get("/")
def health():
return {"status": "ByteBabyLabs engine running"}

@app.post("/api/ospf/paths")
async def ospf_paths(file: UploadFile, prefix: str = Form(...)):
content = (await file.read()).decode("utf-8", errors="ignore")
result = analyze_ospf(content, prefix)
return result
EOF

# ospf_parser.py

cat << 'EOF' > ospf_parser.py
import re

def analyze_ospf(text, prefix):

```
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
```

EOF

echo ""
echo "Bootstrap complete!"
echo "Now run the following commands:"
echo ""
echo "cd api"
echo "pip install -r requirements.txt"
echo "uvicorn main:app --reload --port 8000"
