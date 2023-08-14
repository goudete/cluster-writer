
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
from config.wiki_writer_config import AppConfig


def main():
    root_dir = '../repos/os_writer'
    dataset_path = "hub://goudete/wiki_writer_dataset"

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
                embeddings=OpenAIEmbeddings(
                    openai_api_key=AppConfig.OPENAI_API_KEY,
                ),
                read_only=False
            )
        ),
        retriever=Retriever(
            vectorstore=DeepLakeProvider.instance(
                dataset_path=dataset_path,
                embeddings=OpenAIEmbeddings(
                    openai_api_key=AppConfig.OPENAI_API_KEY,
                ),
                read_only=True
            ),
            model=ChatOpenAI(
                model='gpt-3.5-turbo',
                openai_api_key=AppConfig.OPENAI_API_KEY
            ),
            chain=ConversationalRetrievalChain
        ),
    )

    writer.write()

if __name__ == '__main__':
    main()