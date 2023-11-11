from typing import List
from promptflow import tool
import numpy


@tool
def aggregate(processed_results: List[str]):
    """
    This tool aggregates the processed result of all lines and log metric.

    :param processed_results: List of the output of line_process node.
    """

    value_results = []

    for result in processed_results:
        value_result = float(result.rstrip('%'))
        value_results.append(value_result)

    # Add your aggregation logic here
    fulfillment_ratio = round(numpy.mean(value_results),2)

    aggregated_results = {
        "fulfillment_ratio": str(fulfillment_ratio)+"%"

    }

    # Log metric
    from promptflow import log_metric
    log_metric(key="fulfillment_ratio", value=aggregated_results["fulfillment_ratio"])

    return aggregated_results

if __name__ == "__main__":
    numbers = ["100%", "100%", "0", "100%", "0", "100%", "80%"]
    accuracy = aggregate(numbers)
    print("The accuracy is", accuracy)

