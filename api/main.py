import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, Form, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from ospf_parser import analyze_ospf


app = FastAPI(title="ByteBabyLabs Network Engine")
COMMENTS_FILE = Path(__file__).with_name("comment_submissions.jsonl")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow any domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "ByteBabyLabs engine running"}


@app.post("/api/ospf/paths")
async def ospf_paths(file: UploadFile, prefix: str = Form(...)):
    content = (await file.read()).decode("utf-8", errors="ignore")
    result = analyze_ospf(content, prefix)
    return result


async def _extract_comment_payload(request: Request) -> dict:
    content_type = request.headers.get("content-type", "").lower()

    if "application/json" in content_type:
        payload = await request.json()
        if not isinstance(payload, dict):
            raise HTTPException(status_code=400, detail="JSON body must be an object")
        return payload

    if (
        "application/x-www-form-urlencoded" in content_type
        or "multipart/form-data" in content_type
    ):
        form = await request.form()
        return dict(form)

    raise HTTPException(
        status_code=415,
        detail="Unsupported content type. Use JSON or form data.",
    )


@app.post("/api/comments")
async def submit_comment(request: Request):
    payload = await _extract_comment_payload(request)

    raw_message = payload.get("comment") or payload.get("message") or payload.get("idea")
    raw_name = payload.get("name") or payload.get("author") or "anonymous"
    raw_email = payload.get("email") or ""
    raw_source = payload.get("source") or "website"

    message = str(raw_message or "").strip()
    name = str(raw_name or "anonymous").strip()[:100]
    email = str(raw_email or "").strip()[:200]
    source = str(raw_source or "website").strip()[:100]

    if not message:
        raise HTTPException(status_code=400, detail="Comment text is required")

    if len(message) > 5000:
        raise HTTPException(status_code=400, detail="Comment is too long")

    entry = {
        "id": str(uuid4()),
        "name": name or "anonymous",
        "email": email,
        "source": source or "website",
        "comment": message,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    COMMENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with COMMENTS_FILE.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=True) + "\n")

    return {
        "status": "saved",
        "message": "Comment received",
        "comment_id": entry["id"],
    }


@app.get("/api/comments")
def list_comments(limit: int = 50):
    if limit < 1 or limit > 200:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 200")

    if not COMMENTS_FILE.exists():
        return {"count": 0, "comments": []}

    comments = []
    with COMMENTS_FILE.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            comments.append(json.loads(line))

    return {"count": min(len(comments), limit), "comments": comments[-limit:][::-1]}
