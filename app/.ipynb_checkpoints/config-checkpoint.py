import torch

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

MODEL_PATH = "artifacts/model.pt"
ENCODER_PATH = "artifacts/encoder.pkl"
SCALER_PATH = "artifacts/scaler.pkl"
LABEL_ENCODER_PATH = "artifacts/label_encoder.pkl"
FEATURE_COLS_PATH = "artifacts/feature_cols.pkl"