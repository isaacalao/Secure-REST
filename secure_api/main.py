from fastapi import FastAPI
from . import schema

app = FastAPI()

# Keep in mind dynamic routes/endpoints should be below static ones

@app.get("/")
async def root():
    return {"message": "This is the root."}

@app.post("/demo")
async def demo_handler(demo: schema.Demo):
    return {"message": { "Demo returns": [demo.title, demo.body] }}
