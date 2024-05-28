import bs4
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_text_splitters import RecursiveCharacterTextSplitter


from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings

from langchain_core.messages import HumanMessage


from dotenv import load_dotenv  
import os  

# Add tracing
from promptflow.tracing import trace



import json


if __name__ == "__main__":
    from promptflow.tracing import start_trace
    from promptflow.core import AzureOpenAIModelConfiguration

    start_trace()

    # Batch run and eval


    from promptflow.client import PFClient

    pf = PFClient()
    data = "testset_clean.csv"  # path to the data file


    rag_flow = "rag/flow.flex.yaml"
    eval_flow = "eval/flow.flex.yaml"
    # create run with the flow function and data
    base_run = pf.run(
        flow=rag_flow,
        data=data,
        column_mapping={
            "question": "${data.question}",
            "directory": "chroma_db",
        },
        stream=True,
    )
    details = pf.get_details(base_run)
    details.head(10)



    # run the flow with existing run
    model_config = AzureOpenAIModelConfiguration(
        connection="yijun-aoai",
        azure_deployment="gpt-4-32k",
    )
    eval_run = pf.run(
        flow=eval_flow,
        init={"model_config": model_config},
        data=data,
        run=base_run,
        column_mapping={  # map the url field from the data to the url input of the flow
            "question:": "${data.question}",
            "context:": "${data.context}",
            "groundtruth": "${data.ground_truth}",
            "answer": "${run.outputs.output}",
            },
            stream=True,
        )
    


    # get the inputs/outputs details of a finished run.
    details = pf.get_details(eval_run)
    details.head(10)

    # view the metrics of the eval run
    metrics = pf.get_metrics(eval_run)
    print(json.dumps(metrics, indent=4))

    # visualize both the base run and the eval run
    # pf.visualize([base_run, eval_run])
    pf.visualize([base_run])



