from ollama import embeddings


class Embedder:

    def __init__(self):

        self.model = "nomic-embed-text"

    def embed(self, text: str):

        response = embeddings(
            model=self.model,
            prompt=text
        )

        return response["embedding"]