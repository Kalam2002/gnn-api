import pickle
import torch
from app.model_architecture import Model
from app.config import *

FEATURE_COLS = pickle.load(open(FEATURE_COLS_PATH, "rb"))

def load_artifacts():
    encoder = pickle.load(open(ENCODER_PATH, "rb"))
    scaler = pickle.load(open(SCALER_PATH, "rb"))
    label_encoder = pickle.load(open(LABEL_ENCODER_PATH, "rb"))

    model = Model(
        ndim_in=len(FEATURE_COLS),
        ndim_out=128,
        edim=len(FEATURE_COLS),
        activation=torch.relu,
        dropout=0.2,
        num_classes=10
    ).to(DEVICE)

    state = torch.load(MODEL_PATH, map_location=DEVICE)
    model.load_state_dict(state)
    model.eval()

    return model, encoder, scaler, label_encoder