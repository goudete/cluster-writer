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

root_dir = "./repos/datapipeline-process"

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
# print("docs length: ", len(docs))

print("Chunking files...")
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
texts = text_splitter.split_documents(docs)
# print(f"Length of texts: {len(texts)}")


print("Creating vectorstore...")
dataset_path = "hub://goudete/readme_writer_vectorstore_path"
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

# These are Deeplake specific filters that can be applied
# def filter(x):
#     # filter based on source code
#     if "something" in x["text"].data()["value"]:
#         return False

#     # filter based on path e.g. extension
#     metadata = x["metadata"].data()["value"]
#     return "only_this" in metadata["source"] or "also_that" in metadata["source"]


# ### turn on below for custom filtering
# # retriever.search_kwargs['filter'] = filter

available_models = {
    "ada": "ada",
    "3.5": "gpt-3.5-turbo",
    "4": "gpt-4",
}
model = ChatOpenAI(model_name=available_models["3.5"])
qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)

questions = [
    "Write a ReadMe with a detailed Quick Start section",
    # "What classes are derived from the Chain class?",
    # "What classes and functions in the ./langchain/utilities/ forlder are not covered by unit tests?",
    # "What one improvement do you propose in code in relation to the class herarchy for the Chain class?",
]
chat_history = []

for question in questions:
    result = qa({"question": question, "chat_history": chat_history})
    chat_history.append((question, result["answer"]))
    print(f"-> **Question**: {question} \n")
    print(f"**Answer**: {result['answer']} \n")
