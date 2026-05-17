from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.schemas import FlowRequest
from app.inference import predict
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import sqlite3
import time
import json

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
        (json.dumps(flows), json.dumps(response), payload["timestamp"])
    )
    conn.commit()

    # ---------------- REAL-TIME PUSH (WebSocket) ----------------
    await manager.broadcast(payload)

    return response

# ---------------- LOGS (Polling fallback) ----------------
@app.get("/logs")
def get_logs(limit: int = 20):
    cursor.execute(
        "SELECT id, request, response, timestamp FROM logs ORDER BY timestamp DESC LIMIT ?",
        (limit,)
    )
    rows = cursor.fetchall()
    result = []
    for row in rows:
        try:
            request_data = json.loads(row[1])
        except Exception:
            request_data = []
        try:
            response_data = json.loads(row[2])
        except Exception:
            response_data = {}
        result.append({
            "id": row[0],
            "request": request_data,
            "response": response_data,
            "timestamp": row[3]
        })
    return result
