from promptflow import tool
from promptflow.connections import CustomConnection
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, AzureChatCompletion
#from semantic_kernel.planning import ActionPlanner
from semantic_kernel.planning import SequentialPlanner
from semantic_kernel.planning import ActionPlanner
from semantic_kernel.core_skills import MathSkill, TextSkill
import asyncio
import json

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(ask: str, model: str, aoai_deployment: str, conn: CustomConnection) -> object:
  llm_service = "AzureOpenAI"
  endpoint = conn.AZURE_OPENAI_API_BASE
  api_key = conn.AZURE_OPENAI_API_KEY
  deployment = aoai_deployment

  kernel = sk.Kernel()
  useAzureOpenAI = True

  #deployment, api_key, endpoint = sk.azure_openai_settings_from_dot_env()
  kernel.add_chat_service(model, AzureChatCompletion(deployment, endpoint, api_key, api_version="2023-07-01-preview"))


  skills_directory = "skills/"
  summarize_skill = kernel.import_semantic_skill_from_directory(skills_directory, "SummarizeSkill")
  writer_skill = kernel.import_semantic_skill_from_directory(skills_directory, "WriterSkill")
  #text_skill = kernel.import_skill(TextSkill(), "TextSkill")
  kernel.import_skill(MathSkill(), "math")
  kernel.import_skill(TextSkill(), "text")

  planner = SequentialPlanner(kernel)
  #planner = ActionPlanner(kernel)

  plan = asyncio.run(planner.create_plan_async(goal=ask))

  result = asyncio.run(plan.invoke_async()).result

  #result = asyncio.run(kernel.run_async(plan)).result

  print(result)
  #result = asyncio.run(plan.invoke_async())
  #result = plan.invoke_async()

  steps = [(step.description, ":", step._state.__dict__) for step in plan._steps]

  return_value = {"result": result, "steps": steps}
  
  return return_value

  # for index, step in enumerate(plan._steps):
  #   print("Step:", index)
  #   print("Description:",step.description)
  #   print("Function:", step.skill_name + "." + step._function.name)
  #   if len(step._outputs) > 0:
  #       print( "  Output:\n", str.replace(result[step._outputs[0]],"\n", "\n  "))




