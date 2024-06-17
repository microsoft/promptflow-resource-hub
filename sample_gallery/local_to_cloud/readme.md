# Bring your local application to cloud

POC (proof-of-concept) is always easy, with the help of different kinds of frameworks, tools in the market, you can build your LLM application even in one day. But after POC, once you want to bring your application to production, there are some things your must consider:

* Quality evaluation.
* Collaboration.
* Security.
* Enterprise readiness.
* LLMOps.

That's where a cloud platform chimes in. Here in the tutorial, we aim to walk you through how to bring your proof-of-concept local LLM application to cloud. 


## Prerequisite: POC in local

Suppose your application is of RAG scenario, developed with Langchain in local.

Run the [notebook](./example2/poc_single_web.ipynb) to build the poc RAG app. 




Note: If your local app is also developed by prompt flow, it is a DAG flow with dag.yaml file, you can skip step 1.


## Step 1: Convert to flex flow, 

Flex flow is a concept in prompt flow, the target user is engineers, the core idea is to build a flow with functions. We support Python and C# languages. For C# example, please refer to []().



Compared with DAG flow, the benefits are:

* Easily bring you local code to cloud, just adding several lines of code, then run in azure.
* Support advanced orchestration. DAG flow is short for Directed Acyclic Graph then no cycle support. If you have advanced orchestration needs like if-else, switch, for each and do while, then it is simple to achieve in python code.

Define a data class for output.

```python
# To define output result class
from typing import TypedDict
class Result(TypedDict):
    output: str
```

Wrap your RAG chain into a function.

```python
def flow_entry(question: str = "What is Task Decomposition?") -> Result: 
    # Your RAG chain script here

    return Result(output=output)
```
Then 
```python
if __name__ == "__main__":
    # Your "load data, chunk, build index script" here.

    # Then invoke the RAG chain.
    result = flow_entry("What is Task Decomposition?")
```

Optionally, you can add prompt tracing to debug.

```python
# Import tracing
from promptflow.tracing import trace

# Add trace decorator 
@trace
def flow_entry(question: str = "What is Task Decomposition?") -> Result: 
    # Your RAG script here

    return Result(output=output)


if __name__ == "__main__":
    # Start trace
    from promptflow.tracing import start_trace
    start_trace()

    # The rest of your code
```


Refer to [rag-flexflow.py]() for complete flex flow code.

By adding these lines of code, you  have converted a RAG chain of Langchain into a flex flow in prompt flow. Then you can evaluate the RAG application by using prompt flow's built-in metrics, for example: Groundedness, Relevance, etc. 

## Evaluate

First you need to prepare a golden dataset. 

We provide a [golden dataset](./example2/testset.csv) to help you evaluate the RAG app. You can refer to this [guideline](../../golden_dataset/copilot-golden-dataset-creation-guidance.md) to learn more on how to create your own golden dataset.


Create a flow.flex.yaml file to define a flow which entry pointing to the python function we defined.


## submit to cloud.