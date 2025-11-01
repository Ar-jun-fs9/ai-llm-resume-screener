from sentence_transformers import SentenceTransformer
import os

# Initialize model as None
_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        print(f"Successfully loaded embedding model: all-MiniLM-L6-v2")
    return _model


def load_models_at_startup():
    """Load all embedding models at startup and print success messages."""
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        print(f"Successfully loaded embedding model: all-MiniLM-L6-v2")
    return _model


def get_embedding(text):
    model = get_model()
    return model.encode(text)
