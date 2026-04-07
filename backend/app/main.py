from fastapi import FastAPI

app = FastAPI(
    title="FlowForge API",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "FlowForge running"}

@app.get("/health")
def health():
    return {"status": "ok"}
