class LANForgeSession:

    def __init__(self):

        self.connected = False

        self.host = None

        self.port = 8080

        self.username = None

        self.password = None

        self.inventory = None

    def connect(self, host):

        self.host = host

        self.connected = True

    def disconnect(self):

        self.connected = False

        self.host = None

        self.inventory = None

    def is_connected(self):

        return self.connected