
class WikiWriter:
    def __init__(self, loader, transformer, retriever):
        self.loader = loader
        self.transformer = transformer
        self.retriever = retriever

    def write(self):
        data = self.loader.load()
        print('DATA', data)
        self.transformer.transform(data)
        self.retriever.retrieve()
