from tools.ssh import SSHManager
from config import *


class LanforgeManager:

    def __init__(self):

        self.ssh = SSHManager(
            LANFORGE_HOST,
            LANFORGE_USERNAME,
            LANFORGE_PASSWORD,
            LANFORGE_PORT
        )

        self.ssh.connect()

    def execute(self, command):

        return self.ssh.execute(command)

    def list_scripts(self):

        command = "find ~/lanforge-scripts/py-scripts -name '*.py'"

        return self.execute(command)

    def python_version(self):

        return self.execute("python3 --version")

    def current_directory(self):

        return self.execute("pwd")

    def list_directory(self):

        return self.execute("ls")

    def close(self):

        self.ssh.close()