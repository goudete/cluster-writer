

class Retriever():
    def __init__(self, vectorstore, model, chain):
        self.vectorstore = vectorstore
        self.model = model
        self.chain = chain

    @staticmethod
    def instance(vectorstore):
        return Retriever(
            vectorstore=vectorstore
        )

    def retrieve(self, query):
        retriever = self.vectorstore.as_retriever()
        retriever.search_kwargs['distance_metric'] = 'cos'
        retriever.search_kwargs['fetch_k'] = 100
        retriever.search_kwargs['maximal_marginal_relevance'] = True
        retriever.search_kwargs['k'] = 10

        qa = self.chain.from_llm(
            model=self.model,
            retriever=retriever
        )

        questions = [
            "What is the purpose of this project?",
        ]

        chat_history = []

        for question in questions:  
            result = qa({"question": question, "chat_history": chat_history})
            chat_history.append((question, result['answer']))
            print(f"-> **Question**: {question} \n")
            print(f"**Answer**: {result['answer']} \n")
