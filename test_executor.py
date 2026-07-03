from agent.lanforge_executor import LANforgeExecutor

executor = LANforgeExecutor(

    host="192.168.207.78"

)

result = executor.prepare(

    "Run dataplane"

)

print()

print(result)