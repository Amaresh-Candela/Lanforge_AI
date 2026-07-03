import os
import json

import faiss
import numpy as np

from rag.embedder import Embedder


KNOWLEDGE_DIR = "knowledge"

INDEX_FILE = "rag/index.faiss"

METADATA_FILE = "rag/metadata.json"


class Indexer:

    def __init__(self):

        self.embedder = Embedder()

        self.documents = []

        self.metadata = []

    def load_documents(self):

        folders = [

            "concepts",

            "scripts",

            "parameters",

            "aliases",

            "commands",

            "dependencies"

        ]

        for folder in folders:

            folder_path = os.path.join(
                KNOWLEDGE_DIR,
                folder
            )

            if not os.path.exists(folder_path):
                continue

            for file in os.listdir(folder_path):

                if not file.endswith(".txt"):
                    continue

                path = os.path.join(
                    folder_path,
                    file
                )

                with open(
                    path,
                    encoding="utf8",
                    errors="ignore"
                ) as f:

                    text = f.read()

                self.documents.append(text)

                self.metadata.append(

                    {

                        "folder": folder,

                        "file": file,

                        "text": text

                    }

                )

    def build(self):

        print()

        print("Loading documents...")

        self.load_documents()

        print(len(self.documents), "documents loaded")

        print()

        print("Generating embeddings...")

        vectors = []

        for i, doc in enumerate(self.documents):

            print(f"{i+1}/{len(self.documents)}")

            embedding = self.embedder.embed(doc)

            vectors.append(embedding)

        vectors = np.array(
            vectors,
            dtype=np.float32
        )

        dimension = vectors.shape[1]

        index = faiss.IndexFlatL2(
            dimension
        )

        index.add(vectors)

        faiss.write_index(
            index,
            INDEX_FILE
        )

        with open(
            METADATA_FILE,
            "w",
            encoding="utf8"
        ) as f:

            json.dump(
                self.metadata,
                f,
                indent=4
            )

        print()

        print("Done.")

        print()

        print("Index saved to", INDEX_FILE)

        print("Metadata saved to", METADATA_FILE)


if __name__ == "__main__":

    Indexer().build()