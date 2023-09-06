import os
import getpass
import pinecone
import openai

os.environ["PINECONE_API_KEY"] = getpass.getpass("Pinecone API Key:")
os.environ["PINECONE_ENV"] = getpass.getpass("Pinecone Environment:")
os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:") #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

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.chains import ConversationalRetrievalChain

#to input data found
loader = TextLoader(".txt")
documents = loader.load()

text_splitter = Chara cterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings_model = OpenAIEmbeddings()

embeddings = embeddings_model.embed_documents(
    [
        "This should be a list of news articles",
        "To be added later"
    ]
)

# initialize pinecone vectorstore 
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),  # find at app.pinecone.io
    environment=os.getenv("PINECONE_ENV"),  # next to api key in console
)

index_name = "citihackathon-langchain"

# First, check if our index already exists. If it doesn't, we create it
if index_name not in pinecone.list_indexes():
    # we create a new index
    pinecone.create_index(
      name=index_name,
      metric='cosine',
      dimension=1536  
)
# OpenAI embedding model `text-embedding-ada-002 uses 1536 dimensions`
docsearch = Pinecone.from_documents(docs, embeddings, index_name=index_name)

#similarity search
  #to input query
query = "Prompt from user"
docs = docsearch.similarity_search(query)

index = pinecone.Index("citihackathon-langchain")
vectorstore = Pinecone(index, embeddings.embed_query, "text") #replace "text"

#Add more data to vector store
vectorstore.add_texts("More text!")

#Pass to ChatGPT to generate
chain = ConversationalRetrievalChain.from_llm(
  llm=ChatOpenAI(model="gpt-3.5-turbo"),
  retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
)

"""
# https://github.com/farukalampro/ai-chatbot-using-Langchain-Pinecone/blob/main/indexing.py

# Loading documents from a directory with LangChain
from langchain.document_loaders import DirectoryLoader

directory = 'data'

def load_docs(directory):
  loader = DirectoryLoader(directory)
  documents = loader.load()
  return documents

documents = load_docs(directory)

# Splitting documents
from langchain.text_splitter import RecursiveCharacterTextSplitter
def split_docs(documents,chunk_size=500,chunk_overlap=20):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(documents)
  return docs

docs = split_docs(documents)

# Creating embeddings
from langchain.embeddings import SentenceTransformerEmbeddings
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

query_result = embeddings.embed_query("")


#Storing embeddings in Pinecone 
import pinecone 
from langchain.vectorstores import Pinecone
pinecone.init(
    api_key="",  # find at app.pinecone.io
    environment=""  # next to api key in console
)
index_name = "langchain-chatbot"
index = Pinecone.from_documents(docs, embeddings, index_name=index_name)
"""