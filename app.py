from agent import AIAgent

agent = AIAgent()

print("=" * 60)
print("LANforge AI Assistant")
print("=" * 60)

while True:

    question = input("\nYou : ")

    if question.lower() == "exit":
        break

    answer = agent.ask(question)

    print("\nAI :", answer)