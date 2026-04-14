from fastapi import FastAPI, UploadFile, Form
from ospf_parser import analyze_ospf

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

@app.post("/api/ospf/paths")
async def ospf_paths(file: UploadFile, prefix: str = Form(...)):
    content = (await file.read()).decode("utf-8", errors="ignore")
    result = analyze_ospf(content, prefix)
    return result
