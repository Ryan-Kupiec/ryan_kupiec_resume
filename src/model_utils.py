# src/model_utils.py
import pickle
from pathlib import Path

BUNDLE_PATH = Path(__file__).parent.parent / "models" / "model_bundle.pkl"

def load_bundle():
    """Returns the dict with models, priors, features, etc."""
    with open(BUNDLE_PATH, "rb") as f:
        return pickle.load(f)