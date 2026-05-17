from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.schemas import FlowRequest
from app.inference import predict
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import sqlite3
import time

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- DATABASE ----------------
conn = sqlite3.connect("logs.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request TEXT,
    response TEXT,
    timestamp REAL
)
""")
conn.commit()

# ---------------- CONNECTION MANAGER ----------------
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, payload: dict):
        dead = []
        for ws in self.active_connections:
            try:
                await ws.send_json(payload)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws)

manager = ConnectionManager()

# ---------------- WEBSOCKET ----------------
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive by reading incoming frames
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)

# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {"message": "GNN API running"}

# ---------------- PREDICT ----------------
@app.post("/predict")
async def predict_attack(req: FlowRequest):
    flows = [flow.dict() for flow in req.flows]
    preds = predict(flows)

    response = {
        "num_flows": len(preds),
        "predictions": preds.tolist()
    }

    payload = {
        "timestamp": time.time(),
        "request": flows,
        "response": response
    }

    # ---------------- SAVE TO DB ----------------
    cursor.execute(
        "INSERT INTO logs (request, response, timestamp) VALUES (?, ?, ?)",
        (str(flows), str(response), payload["timestamp"])
    )
    conn.commit()

    # ---------------- REAL-TIME PUSH ----------------
    await manager.broadcast(payload)

    return response
