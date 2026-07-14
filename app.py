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

    if agent.executor.conversation.active:

        answer = agent.executor.continue_conversation(
            question
        )

    else:

        answer = agent.ask(question)

    print()

    print("AI :")

    print(answer)

    print()