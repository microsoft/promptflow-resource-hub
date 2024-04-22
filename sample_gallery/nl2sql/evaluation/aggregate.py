from promptflow import tool
from typing import List, Tuple


@tool
def aggregation(
    exact_string_match: List[int],
    execution_accuracy: List[float],
    llms_score: List[float],
    vector_similarity: List[float],
) -> Tuple[float, float, float, float]:

    print("exact_string_match: ", exact_string_match)
    print("execution_accuracy: ", execution_accuracy)
    print("llms_score: ", llms_score)
    print("vector_similarity: ", vector_similarity)

    # total aggregated score of Exact String Match (EM)
    print(
        "Exact Match Accuracy (EM): ", sum(exact_string_match) / len(exact_string_match)
    )

    # total aggragated score of Execution Accuracy (EX)
    print(
        "Execution Accuracy (EX): ", sum(execution_accuracy) / len(execution_accuracy)
    )

    # total aggregated score of Score by LLMs (SL)
    print("Score by LLMs (SL): ", sum(llms_score) / len(llms_score))

    # total aggregated score of Vector Similarity (ES)
    print(
        "Embedding Similarity (ES): ", sum(vector_similarity) / len(vector_similarity)
    )

    return (
        sum(exact_string_match) / len(exact_string_match),
        sum(execution_accuracy) / len(execution_accuracy),
        sum(llms_score) / len(llms_score),
        sum(vector_similarity) / len(vector_similarity),
    )
