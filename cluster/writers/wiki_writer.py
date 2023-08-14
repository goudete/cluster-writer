
class WikiWriter:
    def __init__(self, loader, transformer, retriever):
        self.loader = loader
        self.transformer = transformer
        self.retriever = retriever

    def write(self):
        data = self.loader.load()
        transformed_data = self.transformer.transform(data)
        retrieved_data = self.retriever.retrieve(transformed_data)

        print("Wiki: ", retrieved_data)

        return
