from agent.parameter_resolver import ParameterResolver

resolver = ParameterResolver()

while True:

    script = input("\nScript : ")

    result = resolver.resolve(script)

    print()
    print(result)