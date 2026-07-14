import requests

from agent.session import LANForgeSession
from tools.inventory import Inventory


class SessionManager:

    def __init__(self):

        self.session = LANForgeSession()

    def connect(self, host):

        try:

            r = requests.get(

                f"http://{host}:8080/ports/all",

                timeout=5

            )

            if r.status_code != 200:

                return False, "Unable to connect."

            inventory = Inventory(host)

            self.session.connect(host)

            self.session.inventory = inventory

            return True, "Connected successfully."

        except Exception as e:

            return False, str(e)

    def get_session(self):

        return self.session