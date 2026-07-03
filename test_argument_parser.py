from parser.argument_parser import ArgumentParser

parser = ArgumentParser()

args = parser.parse(
    r"C:\Users\Amaresh.Koti\Downloads\lanforge-scripts-master\lanforge-scripts-master\py-scripts\lf_dataplane_test.py"
)

print()

for arg in args:

    print(arg)