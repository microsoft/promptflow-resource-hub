import json
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from jinja2 import Template


from promptflow.tracing import trace
from promptflow.core import AzureOpenAIModelConfiguration
from promptflow.core._flow import Prompty


from promptflow.connections import AzureOpenAIConnection
from promptflow.tools.aoai import AzureOpenAI



import bs4
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_text_splitters import RecursiveCharacterTextSplitter


from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings




BASE_DIR = Path(__file__).absolute().parent





@dataclass
class Result:
    groundedness: float
    similarity: float


class QnAEvaluator:  
    def __init__(self, model_config: AzureOpenAIModelConfiguration):  
        self.model_config = model_config  
  
    def __call__(self, question: str, context:str, ground_truth: str, answer: str) -> Result:  
        """Evaluate the QnA based on groundedness and similarity."""  
        groundedness_prompty = Prompty.load(  
            source=BASE_DIR / "groundedness.prompty",  
            model={"configuration": self.model_config},  
        )  
        similarity_prompty = Prompty.load(  
            source=BASE_DIR / "similarity.prompty",  
            model={"configuration": self.model_config},  
        )  
        groundedness_output = groundedness_prompty(context=context, answer=answer)  
        similarity_output = similarity_prompty(question=question, ground_truth=ground_truth, answer=answer)  
  
        output = Result(groundedness=groundedness_output, similarity=similarity_output)  
        return output  
  
    def __aggregate__(self, qna_results: list) -> dict:    
        """Aggregate the results."""    
        total = len(qna_results)    
        avg_groundedness = sum(int(r.groundedness) for r in qna_results) / total    
        avg_similarity = sum(int(r.similarity) for r in qna_results) / total    
        return {    
            "average_groundedness": avg_groundedness,    
            "average_similarity": avg_similarity,    
            "total": total,    
            }   




if __name__ == "__main__":
    from promptflow.tracing import start_trace

    import rag_paths
    from rag_flexflow import rag_chain

    start_trace()
    model_config = AzureOpenAIModelConfiguration(
        connection="yijun-aoai",
        azure_deployment="gpt-4-32k",
    )
    evaluator = QnAEvaluator(model_config)

    import pandas as pd  
  
    # Load the data  
    data = pd.read_csv('../testset_clean.csv')  
    

    
    # Read the first row from the data  
    first_row = data.iloc[0]  
    question = first_row['question']  
    context = first_row['contexts']  
    ground_truth = first_row['ground_truth'] 
    print(f"\nquestion:", question)
    
    


    answer = rag_chain(question, directory= "../rag/chroma_db")
    


    
    # question = "What is Task Decomposition?"
    # context = '''Task Decomposition
    #             Chain of thought (CoT; Wei et al. 2022) has become a standard prompting technique for enhancing model performance on complex tasks. The model is instructed to “think step by step” to utilize more test-time computation to decompose hard tasks into smaller and simpler steps. CoT transforms big tasks into multiple manageable tasks and shed lights into an interpretation of the model’s thinking process.
    #             Tree of Thoughts (Yao et al. 2023) extends CoT by exploring multiple reasoning possibilities at each step. It first decomposes the problem into multiple thought steps and generates multiple thoughts per step, creating a tree structure. The search process can be BFS (breadth-first search) or DFS (depth-first search) with each state evaluated by a classifier (via a prompt) or majority vote.
    #             Task decomposition can be done (1) by LLM with simple prompting like "Steps for XYZ.\n1.", "What are the subgoals for achieving XYZ?", (2) by using task-specific instructions; e.g. "Write a story outline." for writing a novel, or (3) with human inputs.
    #             Another quite distinct approach, LLM+P (Liu et al. 2023), involves relying on an external classical planner to do long-horizon planning. This approach utilizes the Planning Domain Definition Language (PDDL) as an intermediate interface to describe the planning problem. In this process, LLM (1) translates the problem into “Problem PDDL”, then (2) requests a classical planner to generate a PDDL plan based on an existing “Domain PDDL”, and finally (3) translates the PDDL plan back into natural language. Essentially, the planning step is outsourced to an external tool, assuming the availability of domain-specific PDDL and a suitable planner which is common in certain robotic setups but not in many other domains.
    #             '''
    # answer = "{'output': 'Task Decomposition refers to the process of breaking down a complex task into smaller, more manageable tasks. It involves thinking step by step to understand and plan the various components of a complicated task. This technique is used to enhance performance on complex tasks, as it allows for more efficient planning and execution by transforming large tasks into multiple simpler steps.'}"
    # ground_truth = "Task Decomposition is a process where a complex task is broken down into smaller, simpler steps. It allows an agent or model to manage and execute tasks more effectively by enhancing the model's performance on complex tasks. Methods for task decomposition can include using simple prompts, task-specific instructions, or human inputs."



    print(f"\nquestion:", question)
    print(f"\ncontext:", context)
    print(f"\nground_truth:", ground_truth)
    print(f"\nanswer:", answer)
    
    # Use the evaluator  
    result = evaluator(question=question, context=context, answer=answer, ground_truth=ground_truth)  
    
    # Print the result  
    print(result)  



    aggregate_result = evaluator.__aggregate__([result])
    print(aggregate_result)