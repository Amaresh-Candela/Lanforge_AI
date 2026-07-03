import os

import chromadb

from rag.embed import Embedder


DATABASE_PATH = "rag/database"

KNOWLEDGE_PATH = "knowledge"


class RAGBuilder:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path=DATABASE_PATH
        )

        self.collection = self.client.get_or_create_collection(
            "lanforge"
        )

        self.embedder = Embedder()

    def ingest(self):

        count = 0

        for root, dirs, files in os.walk(KNOWLEDGE_PATH):

            for file in files:

                if not file.endswith(".txt"):
                    continue

                filepath = os.path.join(root, file)

                with open(
                    filepath,
                    encoding="utf-8",
                    errors="ignore"
                ) as f:

                    text = f.read()

                chunks = self.chunk(text)

                for chunk in chunks:

                    embedding = self.embedder.embed(chunk)

                    self.collection.add(

                        ids=[str(count)],

                        documents=[chunk],

                        embeddings=[embedding],

                        metadatas=[
                            {
                                "file": file
                            }
                        ]
                    )

                    count += 1

        print()

        print("Indexed", count, "chunks")

    def chunk(self, text):

        words = text.split()

        chunks = []

        chunk_size = 250

        for i in range(
            0,
            len(words),
            chunk_size
        ):

            chunk = " ".join(
                words[
                    i:i + chunk_size
                ]
            )

            chunks.append(chunk)

        return chunks


builder = RAGBuilder()

builder.ingest()