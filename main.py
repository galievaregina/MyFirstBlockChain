import argparse
from gevent import monkey
from blockchain import start

monkey.patch_all()
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('server_id', nargs='?')
    service_id = int(parser.parse_args().server_id)
    start(service_id)
