from langchain_openai import OpenAIEmbeddings


class Memory:
    def __init__(self, **kwargs):
        self._embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    def get_embeddings(self):
        return self._embeddings
