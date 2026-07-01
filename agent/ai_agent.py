from ollama import chat

from config import MODEL

from agent.router import Router
from agent.terminal_generator import TerminalGenerator
from agent.output_explainer import OutputExplainer

from tools.terminal import run_terminal


class AIAgent:

    def __init__(self):

        self.messages = []

        self.router = Router()

        self.generator = TerminalGenerator()

        self.explainer = OutputExplainer()

    def ask(self, question):

        # Decide which tool should handle the request
        intent = self.router.route(question)

        print(f"\nINTENT : {intent}")

        # -------------------------------
        # TERMINAL
        # -------------------------------
        if intent == "terminal":

            command = self.generator.generate(question)

            print(f"COMMAND : {command}")

            result = run_terminal(command)

            output = result["stdout"]

            if output.strip() == "":
                output = result["stderr"]

            return self.explainer.explain(
                question,
                command,
                output
            )

        # -------------------------------
        # LANFORGE (Coming Soon)
        # -------------------------------
        elif intent == "lanforge":

            return "LANforge tool is not implemented yet."

        # -------------------------------
        # REPORTS (Coming Soon)
        # -------------------------------
        elif intent == "report":

            return "Report reader is not implemented yet."

        # -------------------------------
        # RAG (Coming Soon)
        # -------------------------------
        elif intent == "rag":

            return "RAG search is not implemented yet."

        # -------------------------------
        # NORMAL CHAT
        # -------------------------------
        self.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        response = chat(
            model=MODEL,
            messages=self.messages
        )

        answer = response["message"]["content"]

        self.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        return answer