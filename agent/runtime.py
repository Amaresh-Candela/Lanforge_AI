class LANForgeRuntime:

    def __init__(self):

        self.connected = False

        self.host = None

        self.username = None

        self.password = None

        self.ssh = None

        self.raw = {}

        self.interfaces = {}

        self.stations = {}

        self.radios = {}

        self.ethernet = {}

        self.resources = {}

        self.current_execution = None

    def reset(self):

        self.connected = False

        self.host = None

        self.username = None

        self.password = None

        self.ssh = None

        self.raw = {}

        self.interfaces = {}

        self.stations = {}

        self.radios = {}

        self.ethernet = {}

        self.resources = {}

        self.current_execution = None