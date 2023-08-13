from loaders import DataLoader
from transformers import DataTransformer
from retrievers import DataRetriever

class DocumentationWriter:
    def __init__(self, dataLoader, dataTransformer, dataRetriever):
        self.dataLoader = dataLoader
        self.dataTransformer = dataTransformer
        self.dataRetriever = dataRetriever

    def write_documentation(self):
        data = self.dataLoader.load_data()
        transformed_data = self.dataTransformer.transform_data(data)
        retrieved_data = self.dataRetriever.retrieve_data(transformed_data)

        print("Documentation: ", retrieved_data)


def main():
    writer = DocumentationWriter(
        dataLoader=DataLoader(),
        dataTransformer=DataTransformer(),
        dataRetriever=DataRetriever(),
    )

    writer.write_documentation()

if __name__ == '__main__':
    main()