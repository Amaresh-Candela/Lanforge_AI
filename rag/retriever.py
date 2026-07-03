import json

import faiss
import numpy as np

from rag.embedder import Embedder


INDEX_FILE = "rag/index.faiss"

METADATA_FILE = "rag/metadata.json"


class Retriever:

    def __init__(self):

        self.embedder = Embedder()

        self.index = faiss.read_index(
            INDEX_FILE
        )

        with open(
            METADATA_FILE,
            encoding="utf8"
        ) as f:

            self.metadata = json.load(f)

    def search(
        self,
        question,
        top_k=5
    ):

        embedding = self.embedder.embed(question)

        query = np.array(
            [embedding],
            dtype=np.float32
        )

        distances, indices = self.index.search(
            query,
            top_k
        )

        results = []

        for idx in indices[0]:

            if idx < 0:
                continue

            results.append(
                self.metadata[idx]
            )

        return results