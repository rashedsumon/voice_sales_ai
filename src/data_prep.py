import os
import pandas as pd

def load_kaggle_dataset(path="/kaggle/input/call-center-transcripts-dataset"):
    """
    Load dataset. Adjust depending on dataset file names.
    Expects CSV files or JSONL transcripts.
    """
    # try common file names
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset path not found: {path}")
    # find first csv
    files = [f for f in os.listdir(path) if f.lower().endswith(".csv")]
    if not files:
        raise FileNotFoundError("No CSV files found in dataset folder.")
    df = pd.read_csv(os.path.join(path, files[0]))
    return df

def prepare_intent_training(df, text_column="transcript", label_column="intent"):
    """
    Simplified function to obtain X,y for intent classifier training.
    Assumes dataset has transcript text and (optionally) labels.
    """
    if label_column not in df.columns:
        print("No label column found; you'll need to label data for supervised training.")
        return df[text_column].tolist(), None
    X = df[text_column].astype(str).tolist()
    y = df[label_column].astype(str).tolist()
    return X, y
