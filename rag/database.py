import chromadb


class VectorDatabase:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="rag/database"
        )

    def get_collection(self, name):

        return self.client.get_or_create_collection(
            name=name
        )

    def delete_collection(self, name):

        try:
            self.client.delete_collection(name)
        except:
            pass

    def list_collections(self):

        return self.client.list_collections()