from agent.parameter_resolver import ParameterResolver


resolver = ParameterResolver()

question = "Run dataplane test"

result = resolver.resolve(question)

print(result)