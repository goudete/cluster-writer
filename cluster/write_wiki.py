
# Dependencies
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain


# Custom Dependencies
from writers.wiki_writer import WikiWriter
from loaders.manual_loader import ManualLoader
from transformers.transformer import Transformer
from retrievers.retriever import Retriever
from vectorstores.deep_lake import DeepLakeProvider


def main():
    root_dir = '../repos/os_writer'
    dataset_path = "hub://goudete/readme_writer_vectorstore_path"

    writer = WikiWriter(
        loader=ManualLoader(
            root_dir=root_dir
        ),
        transformer=Transformer(
            splitter=CharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=0
            ),
            vectorstore=DeepLakeProvider.instance(
                dataset_path=dataset_path,
                embeddings=OpenAIEmbeddings(),
                read_only=False
            )
        ),
        retriever=Retriever.instance(
            vectorstore=DeepLakeProvider.instance(
                dataset_path=dataset_path,
                embeddings=OpenAIEmbeddings(),
                read_only=True
            ),
            model=ChatOpenAI(model='gpt-3.5-turbo'), # switch to 'gpt-4'
            chain=ConversationalRetrievalChain
        ),
    )

    writer.write()

if __name__ == '__main__':
    main()