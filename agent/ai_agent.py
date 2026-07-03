from ollama import chat

from config import MODEL

from agent.intent_classifier import IntentClassifier
from agent.planner import Planner
from agent.memory import Memory

from tools.router import Router
from tools.terminal_generator import TerminalGenerator

from rag.retriever import Retriever

from agent.conversation_state import ConversationState

from agent.lanforge_executor import LANforgeExecutor


class AIAgent:

    def __init__(self):

        self.memory = Memory()

        self.classifier = IntentClassifier()

        self.planner = Planner()

        self.router = Router()

        self.generator = TerminalGenerator()

        self.rag = Retriever()
        self.state = ConversationState()

        self.executor = LANforgeExecutor(

            host="192.168.207.78"

        )

    def ask(self, question):

        # -------------------------
        # 1. Intent Classification
        # -------------------------

        intent = self.classifier.classify(question)

        print(f"\nINTENT : {intent}")

        # -------------------------
        # 2. Planning
        # -------------------------

        plan = self.planner.plan(intent, question)

        # -------------------------
        # 3. Terminal Execution
        # -------------------------

        if plan["tool"] == "terminal":

            command = self.generator.generate(question)

            print(f"\nCOMMAND : {command}")

            plan["command"] = command

            return self.router.execute(plan)

        # -------------------------
        # 4. RAG Search
        # -------------------------
        elif plan["tool"] == "lanforge":

            result = self.executor.prepare(question)

            return result
        
        elif plan["tool"] == "rag":

            docs = self.rag.search(question)

            context = ""

            for doc in docs:

                context += f"""

File : {doc['file']}

Folder : {doc['folder']}

Content:

{doc['text']}

====================================================
"""

            prompt = f"""
You are an expert LANforge assistant.

Answer ONLY using the documentation provided below.

If the answer is not present in the documentation,
reply exactly:

I could not find this in the LANforge documentation.

Documentation:

{context}

User Question:

{question}

Answer:
"""

            self.memory.add_user(question)

            response = chat(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": prompt
                    }
                ] + self.memory.get()
            )

            answer = response["message"]["content"]

            self.memory.add_assistant(answer)

            return answer

        # -------------------------
        # 5. Normal Chat
        # -------------------------

        self.memory.add_user(question)

        response = chat(
            model=MODEL,
            messages=self.memory.get()
        )

        answer = response["message"]["content"]

        self.memory.add_assistant(answer)

        return answer