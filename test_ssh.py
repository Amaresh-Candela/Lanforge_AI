from tools.ssh import SSHManager

from config import *


ssh = SSHManager(
    LANFORGE_HOST,
    LANFORGE_USERNAME,
    LANFORGE_PASSWORD,
    LANFORGE_PORT
)

ssh.connect()

result = ssh.execute("pwd")

print(result["stdout"])

ssh.close()