try:
    from ._miniops import vector_add, topk, softmax
    BACKEND = "native"
except ImportError:
    from .reference import vector_add, topk, softmax
    BACKEND = "reference"

__all__ = ["vector_add", "topk", "softmax", "BACKEND"]
