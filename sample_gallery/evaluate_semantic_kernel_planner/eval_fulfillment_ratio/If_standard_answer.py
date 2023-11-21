from promptflow import tool

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(groundtruth_answer: str) -> bool:
  is_standard_answer = False
  if groundtruth_answer == 'no standard answer':
    is_standard_answer = True
  return is_standard_answer
