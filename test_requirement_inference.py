from parser.requirement_inference import RequirementInference

infer = RequirementInference()

required = infer.infer(
    r"C:\Users\Amaresh.Koti\Downloads\lanforge-scripts-master\lanforge-scripts-master\py-scripts\lf_dataplane_test.py"
)

print()

print("Required Parameters\n")

for r in required:

    print(r)