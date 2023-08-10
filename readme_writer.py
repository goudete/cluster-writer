import os

from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import DeepLake
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader


# Keys
os.environ['OPENAI_API_KEY'] = "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"
os.environ["ACTIVELOOP_TOKEN"] = "eyJhbGciOiJIUzUxMiIsImlhdCI6MTY5MDkzNjA3OSwiZXhwIjoxNjkzNTI4MDE5fQ.eyJpZCI6ImdvdWRldGUifQ.zE7lPgIANl-Ok63E4K7T397F8VTNwPA-DaUHYk-4I7VZdTNFpxW65bHJ9-IGvTdHJF2lDbPa9I9vBFQBQCM75A"

root_dir = "./repos/os_writer"

print("Extracting repository files...")
docs = []
for dirpath, dirnames, filenames in os.walk(root_dir):
  for file in filenames:
    if file.endswith(".py") and "/.venv/" not in dirpath:
      try:
          loader = TextLoader(
            os.path.join(
              dirpath,
              file
            ),
            encoding="utf-8"
          )
          docs.extend(loader.load_and_split())
      except Exception as e:
        pass

print("Chunking files...")
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
texts = text_splitter.split_documents(docs)


print("Creating vectorstore...")
dataset_path = "hub://goudete/readme-writer-os-writer"
# Creating new vectorstore
db = DeepLake.from_documents(
    texts,
    dataset_path=dataset_path,
    embedding=OpenAIEmbeddings()
)

retriever = db.as_retriever()
retriever.search_kwargs["distance_metric"] = "cos"
retriever.search_kwargs["fetch_k"] = 100
retriever.search_kwargs["maximal_marginal_relevance"] = True
retriever.search_kwargs["k"] = 10


available_models = {
    "ada": "ada",
    "3.5": "gpt-3.5-turbo",
    "4": "gpt-4",
}
model = ChatOpenAI(model_name=available_models["3.5"])
qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)

question = "Write a ReadMe with a detailed Quick Start section about how to run the project."

result = qa({"question": question, "chat_history": []})

print(f"**Answer**: {result['answer']} \n")
