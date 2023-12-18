# QUERYING EXISTING VECTOR INDEXES WITH PROMPTFLOW

To query existing vector indexes in a PromptFlow standard or chat flow, a [Vector DB Lookup tool](https://learn.microsoft.com/en-us/azure/machine-learning/prompt-flow/tools-reference/vector-db-lookup-tool) is used. Vector DB Lookup tool is a wrapper for Azure AI Search as well as multiple third-party vector databases such as Qdrant and Weaviate.

In this sample, we will go over how to query an existing vector index on Azure AI Search.

The document we use is the "World Economic Outlook" document from 10th October 2023. (You can download the document [here](https://www.imf.org/en/Publications/WEO)). We assume the document is already chunked and its embeddings stored in an AI Search vector index named "worldeconomyoctober".  

Vector DB Lookup tool requires a set of required and optional "inputs" depending on the vector db used documented [here](https://learn.microsoft.com/en-us/azure/machine-learning/prompt-flow/tools-reference/vector-db-lookup-tool?view=azureml-api-2). For AI Search the required parameters are the AI Search connection to be used, the index name on AI Search, vector_field name, the vector to be queried (question embedding in our case from the earlier flow step).

For further info please refer to the blog post [here](https://medium.com/@343544/azure-promptflow-querying-existing-vectordb-indexes-55af636e02fb).
