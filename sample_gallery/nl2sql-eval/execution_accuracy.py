from promptflow import tool
from typing import Tuple


@tool
def execution_accuracy(
    queried_data: Tuple[list, list, bool],
) -> float:

    value_groundtruth = queried_data[0]
    value_generated = queried_data[1]
    order_by = queried_data[2]

    ex = evaluate(value_groundtruth, value_generated, order_by)

    return ex


# Score of Execution Accuracy (EX)
def evaluate(value_groundtruth, value_generated, order_by: bool) -> float:

    # compare value_groundtruth and value_generated. If order_by is True, compare value_groundtruth and value_generated (don't use set)
    if order_by:
        for i in range(len(value_groundtruth)):
            if value_groundtruth[i] != value_generated[i]:
                count = 0
                break
            else:
                count = 1
        score = count / len(value_groundtruth)
    # compare value_groundtruth and value_generated regardless of the order of the elements.
    elif set(value_groundtruth) == set(value_generated):
        score = 1
    # count the number of elements of intersection between value_groundtruth and value_generated, and divide it by the number of elements of value_groundtruth.
    elif set(value_groundtruth) != set(value_generated):
        score = len(set(value_groundtruth).intersection(set(value_generated))) / len(
            set(value_groundtruth)
        )
    else:
        score = 0
    return score
