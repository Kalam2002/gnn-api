from fastapi import FastAPI
from app.schemas import FlowRequest
from app.inference import predict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/predict")
def predict_attack(req: FlowRequest):
    flows = [flow.dict() for flow in req.flows]
    preds = predict(flows)
    return {
        "num_flows": len(preds),
        "predictions": preds.tolist()
    }