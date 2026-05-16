from fastapi import FastAPI, WebSocket
from app.schemas import FlowRequest
from app.inference import predict
from fastapi.middleware.cors import CORSMiddleware

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

# ---------------- WEBSOCKET ----------------
active_connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)

    try:
        while True:
            await websocket.receive_text()
    except:
        active_connections.remove(websocket)

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

    # Combine request + response
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
    for ws in active_connections:
        await ws.send_json(payload)

    return response
