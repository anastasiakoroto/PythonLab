from const import SERVERS_HOST, SERVER_TWO_PORT
from base import BaseServer, run


class ServerTwo(BaseServer):
    pass


if __name__ == '__main__':
    run(SERVERS_HOST, SERVER_TWO_PORT, ServerTwo)
