from parser.import_parser import ImportParser

parser = ImportParser()

imports = parser.parse(
    r"C:\Users\Amaresh.Koti\Downloads\lanforge-scripts-master\lanforge-scripts-master\py-scripts\lf_dataplane_test.py"
)

for module in imports:

    print(module)