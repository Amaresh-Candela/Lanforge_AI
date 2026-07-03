from rag.retriever import Retriever


rag = Retriever()

while True:

    question = input("\nQuestion : ")

    docs = rag.search(question)

    print()

    for i, doc in enumerate(docs, 1):

        print("=" * 60)

        print(i)

        print()

        print("Folder :", doc["folder"])

        print("File   :", doc["file"])

        print()

        print(doc["text"])