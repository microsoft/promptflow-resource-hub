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
  
# Load the .env file  
load_dotenv()  
  
# Get an environment variable  
endpoint = os.getenv('AZURE_OPENAI_ENDPOINT') 
key = os.getenv('AZURE_OPENAI_API_KEY')
api_version = os.getenv('AZURE_OPENAI_API_VERSION')  
chat_deployment = os.getenv('AZURE_OPENAI_CHAT_DEPLOYMENT')  
embedding_deployment = os.getenv('AZURE_OPENAI_EMBEDDING_DEPLOYMENT')


chat = AzureChatOpenAI(
    azure_deployment=chat_deployment,
    openai_api_version=api_version,
)

# Test chat openai, you can uncommment to test if your enviroment variable is correctly set up.
# message = HumanMessage(
#     content="Translate this sentence from English to French. I love programming."
# )
# result = chat.invoke([message]) 
# print(result.content)  
  





def rag_chain(question: str = "What is Task Decomposition?", directory: str = "./chroma_db"):

    # directory where the index will be saved/loaded from  
    # Load the .env file  
    load_dotenv()  
    
    # Get an environment variable  
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT') 
    key = os.getenv('AZURE_OPENAI_API_KEY')
    api_version = os.getenv('AZURE_OPENAI_API_VERSION')  
    embedding_deployment = os.getenv('AZURE_OPENAI_EMBEDDING_DEPLOYMENT')


    # Get an environment variable  
    embedding_deployment = os.getenv('AZURE_OPENAI_EMBEDDING_DEPLOYMENT')


    embedding=AzureOpenAIEmbeddings(
        azure_deployment=embedding_deployment,
        openai_api_version=api_version,)



    
    if os.path.exists(directory):  
        print(f"Index exists, loading") 
        # if the directory exists, load the index  
        vectorstore = Chroma(persist_directory=directory, embedding_function=embedding)

    else:  
        print(f"Index not exist, building") 
        # if the directory does not exist, create the index and save it  

        # Load, chunk and index the contents of the blog.
        loader = WebBaseLoader(
            web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
            bs_kwargs=dict(
                parse_only=bs4.SoupStrainer(
                    class_=("post-content", "post-title", "post-header")
                )
            ),
        )
        docs = loader.load()


        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)

        vectorstore = Chroma.from_documents(documents=splits, embedding=embedding, persist_directory=directory)  

    # Retrieve and generate using the relevant snippets of the blog.
    retriever = vectorstore.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)


    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | chat
        | StrOutputParser()
    )
    return rag_chain.invoke(question)


if __name__ == "__main__":
    

    
    import pandas as pd  
  
    # Load the data  
    data = pd.read_csv('testset_question.csv') 

    # Create an empty DataFrame to store the question and answers  
    results = pd.DataFrame(columns=['question', 'answer'])      
    
    # Iterate over the questions in the data  
    for index, row in data.iterrows():  
        question = row['question']  
       
        
        # Generate the answer using the rag_chain function  
        answer = rag_chain(question) 
        print(answer) 
        
        # Append the question and answer to the results DataFrame  
        results.loc[index] = [question, answer]  
  
    # Save the results DataFrame to a new CSV file  
    results.to_csv('testset_question_answer.csv', index=False)  
    
         

    