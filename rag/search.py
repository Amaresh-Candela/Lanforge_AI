import chromadb

from rag.embed import Embedder


DATABASE_PATH = "rag/database"


class RAGSearcher:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path=DATABASE_PATH
        )

        self.collection = self.client.get_collection(
            "lanforge"
        )

        self.embedder = Embedder()

    def search(

        self,

        question,

        k=5

    ):

        embedding = self.embedder.embed(question)

        result = self.collection.query(

            query_embeddings=[
                embedding
            ],

            n_results=k
        )

        return result["documents"][0]