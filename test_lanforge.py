from tools.lanforge import LanforgeManager

lf = LanforgeManager()

print("\nCurrent Directory\n")
print(lf.current_directory()["stdout"])

print("\nPython Version\n")
print(lf.python_version()["stdout"])

print("\nScripts\n")

result = lf.list_scripts()

print(result["stdout"])

lf.close()