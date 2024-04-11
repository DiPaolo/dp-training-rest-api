import sys
from typing import Optional

from web_server.flask_impl.web_server import start


def parse_args() -> Optional[str]:
    if len(sys.argv) != 2:
        return None
    return sys.argv[1]


if __name__ == '__main__':
    cmd = parse_args()

    if cmd == 'parse':
        # from parser.parser import get_forecast_data
        # from repository import update_repo
        # import pprint
        #
        # data = get_forecast_data()
        # update_repo(data)
        # print('Updated with data:')
        # pprint.pprint(data)
        pass
    elif cmd == 'get':
        from web_server.repository import get_repo
        import pprint

        data = get_repo()
        pprint.pprint(data)
    elif cmd == 'server':
        start()
    else:
        print('ERROR unknown command. Available commands: parse, get, server')
