from promptflow import tool
import re


@tool
def extract_score(llms_output: str) -> float:
    # first integar (0~5) in the string (llms_output) using re
    match = re.findall(r"\b[0-5]\b", llms_output)
    print("match", match)
    if not match:
        return 0.0
    else:
        return int(match[0]) / 5
