import os
import pandas as pd

def load_kaggle_dataset(dataset_path: str = "/kaggle/input/call-center-transcripts-dataset") -> pd.DataFrame:
    """
    Loads a Kaggle dataset from the specified path.
    Expects one or more CSV files within the directory.

    Parameters:
        dataset_path (str): Path to the dataset folder.

    Returns:
        pd.DataFrame: Loaded dataset as a pandas DataFrame.

    Raises:
        FileNotFoundError: If the dataset path or CSV file is missing.
    """
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"❌ Dataset path not found: {dataset_path}")

    # Identify CSV files in the directory
    csv_files = [file for file in os.listdir(dataset_path) if file.lower().endswith(".csv")]
    if not csv_files:
        raise FileNotFoundError("❌ No CSV files found in the dataset folder.")

    # Load the first CSV file
    file_path = os.path.join(dataset_path, csv_files[0])
    print(f"✅ Loading dataset from: {file_path}")
    return pd.read_csv(file_path)


def prepare_intent_training(df: pd.DataFrame, text_column: str = "transcript", label_column: str = "intent"):
    """
    Prepares input features (X) and labels (y) for intent classification.

    Parameters:
        df (pd.DataFrame): Input dataset.
        text_column (str): Name of the column containing conversation text.
        label_column (str): Name of the column containing intent labels.

    Returns:
        tuple: (X, y)
            X -> List of text samples.
            y -> List of intent labels, or None if labels are missing.
    """
    if text_column not in df.columns:
        raise ValueError(f"❌ Text column '{text_column}' not found in dataset.")

    if label_column not in df.columns:
        print("⚠️ No label column found. Returning text only for unsupervised or manual labeling.")
        return df[text_column].astype(str).tolist(), None

    X = df[text_column].astype(str).tolist()
    y = df[label_column].astype(str).tolist()
    print(f"✅ Prepared {len(X)} samples for intent classification training.")
    return X, y
