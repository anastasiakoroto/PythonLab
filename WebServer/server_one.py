from base import BaseServer, run
from const import SERVERS_HOST, SERVER_ONE_PORT


class ServerOne(BaseServer):
    pass


if __name__ == '__main__':
    run(SERVERS_HOST, SERVER_ONE_PORT, ServerOne)
