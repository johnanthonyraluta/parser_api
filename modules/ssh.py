import pexpect
from decouple import config
import sys

class Tunnel:
    def __init__(self):
        try:
            ssh_command = f"ssh {config('SSH_TUNNEL')} -D 1080"
            self.connection = pexpect.spawn(ssh_command)
            self.connection.expect("\$\s+$")
        except Exception as err:
            print(err)

    def disconnect(self):
        self.connection.close()