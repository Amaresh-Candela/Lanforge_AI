from tools.ssh import SSHManager


class ExecutionRunner:

    def __init__(
        self,
        host,
        username,
        password
    ):

        self.ssh = SSHManager(
            host,
            username,
            password
        )

        self.ssh.connect()

    def run(self, command):

        return self.ssh.execute(command)