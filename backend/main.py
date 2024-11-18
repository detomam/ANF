from fastapi import FastAPI
from backend.endpoints import websocket, query, data

app = FastAPI()

# Include routes from different modules
app.include_router(websocket.router)
app.include_router(query.router)
app.include_router(data.router)

@app.get("/")
def home():
    return {"message": "Backend is running"}
