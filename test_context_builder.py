from knowledge.context_builder import ContextBuilder

builder = ContextBuilder()

context = builder.build(
    "lf_dataplane_test.py"
)

print(context.keys())

print()

print(context["script"]["name"])

print()

print(context["source"][:1500])