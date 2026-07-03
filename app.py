from agent.ai_agent import AIAgent

agent = AIAgent()

print()

print("LANForge AI Ready")

print()

while True:

    question = input("You : ")

    if question.lower() in [

        "exit",

        "quit"

    ]:

        break

    answer = agent.ask(question)

    print()

    print("AI :")

    print(answer)

    print()