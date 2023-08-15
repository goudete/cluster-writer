
class WikiWriter:
    def __init__(self, loader, transformer):
        self.loader = loader
        self.transformer = transformer
        # self.retriever = retriever

    def write(self):
        data = self.loader.load()
        self.transformer.transform(data)
