import numpy as np
import pandas as pd

def preprocess(df, encoder, scaler, feature_cols):

    # 🔥 STEP 1: match encoder input columns (NOT feature_cols)
    trained_cols = list(encoder.feature_names_in_)

    for col in trained_cols:
        if col not in df.columns:
            df[col] = 0

    # keep ONLY encoder columns
    df = df[trained_cols]

    # 🔥 STEP 2: apply encoder
    df = encoder.transform(df)

    # 🔥 STEP 3: NOW select model features (60 cols)
    df = df[feature_cols]

    # 🔥 STEP 4: numeric conversion
    df = df.apply(pd.to_numeric, errors='coerce').fillna(0)

    # 🔥 STEP 5: scaling
    try:
        df = pd.DataFrame(scaler.transform(df), columns=df.columns)
    except:
        pass

    return df.astype(np.float32).values.tolist()