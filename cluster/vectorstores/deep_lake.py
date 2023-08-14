from langchain.vectorstores import DeepLake

class DeepLakeProvider():
    def __init__(self, db):
        self.db = db

    @staticmethod
    def instance(dataset_path, embeddings, read_only=False):
        db = DeepLake(
            dataset_path=dataset_path,
            embedding_function=embeddings,
            read_only=read_only
        )
        return DeepLakeProvider(
            db=db
        )