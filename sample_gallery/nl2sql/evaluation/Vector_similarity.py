from promptflow import tool
import numpy as np
from numpy.linalg import norm


@tool
def compute_cosine_cosine_similarity(
    groundtruth_embedding, generated_embedding
) -> float:
    return np.dot(groundtruth_embedding, generated_embedding) / (
        norm(groundtruth_embedding) * norm(generated_embedding)
    )
