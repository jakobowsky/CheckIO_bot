import json


def read_credentials():
    # secrets
    secrets = 'secrets.json'
    with open(secrets) as f:
        keys = json.loads(f.read())
        return keys

class CheckIOSolver:
    def __init__(self, login, password):
        self.login = login
        self.password = password


if __name__ == '__main__':
    credentials = read_credentials()
    bot = CheckIOSolver(credentials['username'], credentials['password'])
    