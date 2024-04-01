from promptflow import tool
from typing import Tuple


@tool
def exact_string_match(
    sql_groundtruth: str,
    sql_generated: str,
) -> int:

    sql_groundtruth = sql_groundtruth.lower()
    sql_generated = sql_generated.lower()

    em = evaluate(sql_groundtruth, sql_generated)

    return em


# Score of Exact String Accuracy (EM)
def evaluate(sql_groundtruth, sql_generated):

    # compare sql_groundtruth and sql_generated.
    if sql_groundtruth == sql_generated:
        count = 1
    else:
        count = 0

    return count
