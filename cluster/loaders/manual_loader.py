import os
from langchain.document_loaders import TextLoader


class ManualLoader():

    def __init__(self, root_dir):
        self.root_dir = root_dir

    def load(self):
        print('ROOT DIR', self.root_dir)
        docs = []
        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            for file in filenames:
                print('FILE', file)
                try:
                    loader = TextLoader(
                        os.path.join(dirpath, file),
                        encoding='utf-8'
                    )
                    docs.extend(loader.load_and_split())
                except Exception as e:
                    pass

        print('DOCS IN MANUAL LOADER', docs)
        return docs