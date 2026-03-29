import pandas as pd
import torch
from app.model_loader import load_artifacts, FEATURE_COLS
from app.preprocess import preprocess
from app.graph_builder import build_graph
from app.config import DEVICE

model, encoder, scaler, label_encoder = load_artifacts()

def predict(flows):
    df = pd.DataFrame(flows)

    # 🔥 same as training
    df["src_ip"] = df["src_ip"].astype(str) + ":" + df["src_port"].astype(str)
    df["dst_ip"] = df["dst_ip"].astype(str) + ":" + df["dst_port"].astype(str)

    h = preprocess(df, encoder, scaler, FEATURE_COLS)

    G = build_graph(df, h, DEVICE)

    with torch.no_grad():
        logits = model(G, G.ndata["h"], G.edata["h"])
        preds = logits.argmax(1).cpu().numpy()

    return label_encoder.inverse_transform(preds)