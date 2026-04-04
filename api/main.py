from fastapi import FastAPI, UploadFile, Form
from ospf_parser import analyze_ospf
from pydantic import BaseModel, EmailStr
from datetime import datetime
import json
import os

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="ByteBabyLabs Network Engine")

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

class CommentSubmission(BaseModel):
    email: EmailStr
    comment: str

@app.post("/api/comments")
async def submit_comment(submission: CommentSubmission):
    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "email": submission.email,
        "comment": submission.comment,
    }
    comment_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tools", "comments.txt"))
    with open(comment_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return {"status": "ok", "record": record}

@app.post("/api/ospf/paths")
async def ospf_paths(file: UploadFile, prefix: str = Form(...)):
    content = (await file.read()).decode("utf-8", errors="ignore")
    result = analyze_ospf(content, prefix)
    return result
