

class Transformer():
    
    def __init__(self, splitter, vectorstore):
        self.splitter = splitter
        self.vectorstore = vectorstore

    def transform(self, docs):
        '''
        Split documents into chunks
        Index the chunks (embeddings)
        '''
        texts = self.split(docs)
        self.index(texts)
        return

    def split(self, docs):
        texts = self.splitter.split_documents(docs)
        return texts
    
    def index(self, docs):
        self.vectorstore.add_documents(docs)
        return