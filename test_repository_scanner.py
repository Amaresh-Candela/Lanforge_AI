from parser.repository_scanner import RepositoryScanner

ROOT = r"C:\Users\Amaresh.Koti\Downloads\lanforge-scripts-master\lanforge-scripts-master"
scanner = RepositoryScanner(ROOT)

print(f"Repository Root : {ROOT}")
print()

all_files = scanner.scan()

print(f"Total Python Files : {len(all_files)}")
print()

print("=" * 80)
print("First 20 Python Files")
print("=" * 80)

for file in all_files[:20]:
    print(file)

print()

print("=" * 80)
print("PY-SCRIPTS")
print("=" * 80)

scripts = scanner.scan_py_scripts()

print(f"Found : {len(scripts)}")

for file in scripts[:20]:
    print(file)

print()

print("=" * 80)
print("PY-JSON")
print("=" * 80)

json_files = scanner.scan_py_json()

print(f"Found : {len(json_files)}")

for file in json_files[:20]:
    print(file)