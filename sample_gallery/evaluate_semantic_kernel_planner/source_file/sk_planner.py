import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, AzureChatCompletion
#from semantic_kernel.planning import ActionPlanner
from semantic_kernel.planning import SequentialPlanner
from semantic_kernel.planning import ActionPlanner
from semantic_kernel.core_skills import MathSkill, TextSkill
import asyncio

def sk_planner(ask: str, model: str, aoai_deployment: str, api_version: str) -> object:
  llm_service = "AzureOpenAI"
  deployment_name, api_key, endpoint = sk.azure_openai_settings_from_dot_env(include_deployment=False)
  api_version = api_version
  deployment = aoai_deployment

  kernel = sk.Kernel()
  useAzureOpenAI = True

  #deployment, api_key, endpoint = sk.azure_openai_settings_from_dot_env()
  kernel.add_chat_service(model, AzureChatCompletion(deployment, endpoint, api_key, api_version))

  skills_directory = "skplanner/sk_planner_flow/skills/"
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

if __name__=="__main__":
    
    ask = """
    Tomorrow is Valentine's day. I need to come up with a few date ideas. She speaks French so write it in French.
    Convert the text to uppercase"""
    model = "gpt-4"
    aoai_deployment = "gpt-4"
    api_version = "2023-07-01-preview"

    sk_planner(ask=ask, model=model , aoai_deployment=aoai_deployment, api_version=api_version)

  # for index, step in enumerate(plan._steps):
  #   print("Step:", index)
  #   print("Description:",step.description)
  #   print("Function:", step.skill_name + "." + step._function.name)
  #   if len(step._outputs) > 0:
  #       print( "  Output:\n", str.replace(result[step._outputs[0]],"\n", "\n  "))




