from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from backend.endpoints import websocket, query, data

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins; adjust to your needs
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Include routes
app.include_router(websocket.router)
app.include_router(query.router)
app.include_router(data.router)

@app.get("/")
def home():
    return {"message": "Backend is running"}
