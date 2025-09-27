# backend/main.py
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from backend.agents.orchestrator import Orchestrator
from backend.sanity_client import save_blog_post
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Dynamic Blog Assistant API")
orchestrator = Orchestrator()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    topic: str
    keywords: str = ""

class SaveRequest(BaseModel):
    title: str
    draft: str
    edits: str
    seo: str

@app.get("/")
async def root():
    return {"status": "ok", "message": "Dynamic Blog Assistant Backend with Gemini & Sanity"}

@app.post("/generate")
async def generate(req: GenerateRequest):
    try:
        result = await orchestrator.generate_blog(req.topic, req.keywords)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/save")
def save(req: SaveRequest):
    try:
        res = save_blog_post(req.title, req.draft, req.edits, req.seo)
        return {"status": "saved", "result": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
