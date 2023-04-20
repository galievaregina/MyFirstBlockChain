import json
import random
import string
from hashlib import sha256
from flask import Flask, request
import time
import threading
import logging
import grequests

class Block:
    def __init__(self, service_id, index, prev_hash):
        self.service_id = service_id
        self.index = index
        self.prev_hash = prev_hash
        self.hash = None
        self.data = None
        self.nonce = 0
        self.generate_data()
        self.generate_correct_hash()

    def generate_correct_hash(self):
        current_hash = sha256(
            (str(self.index) + self.prev_hash + self.data + str(self.nonce)).encode('utf-8')).hexdigest()
        while current_hash[-4:] != "0000":
            self.nonce += random.randint(10, 40)
            current_hash = sha256(
                (str(self.index) + self.prev_hash + self.data + str(self.nonce)).encode('utf-8')).hexdigest()
        self.hash = current_hash

    def generate_data(self):
        self.data = ''.join(random.choice(string.ascii_lowercase) for _ in range(256))

    def get_block_data(self):
        return json.dumps({
            'service_id': self.service_id,
            'index': self.index,
            'hash': self.hash,
            'prev_hash': self.prev_hash,
            'data': self.data,
            'nonce': self.nonce
        })


class Node:
    blocks = []

    def __init__(self, server_id):
        self.server_id = server_id
        self.block_index = None

    def get_input_block(self, received_block):
        input_block = json.loads(received_block)
        input_index = int(input_block['index'])
        if input_index == 0:
            self.blocks.append(received_block)
            self.block_index = 0
            print(f'GENESIS:' + str(input_block))
            return True
        blocks_array_object = json.loads(self.blocks[-1])
        last_block_index = blocks_array_object['index']
        if input_index > last_block_index:
            self.blocks.append(received_block)
            self.block_index = input_index
            if self.server_id != input_block['service_id']:
                print(f'Service{self.server_id} received:' + str(input_block))
            return True
        return False


def start(service):
    current_service = Flask(__name__)
    current_node = Node(service)
    host = 'localhost'
    if service == 1:
        port1, port2, port3 = 5000, 5001, 5002
    elif service == 2:
        port1, port2, port3 = 5001, 5000, 5002
    else:
        port1, port2, port3 = 5002, 5000, 5001
    logging.getLogger('werkzeug').disabled = True
    servers_urls = [f'http://{host}:{port1}/', f'http://{host}:{port2}/', f'http://{host}:{port3}/']

    def create_new_blocks():
        while True:
            if len(current_node.blocks) != 0:
                last_block = json.loads(current_node.blocks[-1])
                prev_hash = last_block['hash']
                new_block = Block(current_node.server_id, current_node.block_index + 1, prev_hash)
                if new_block.index > current_node.block_index:
                    rst = (grequests.post(u, json=new_block.get_block_data()) for u in servers_urls)
                    grequests.map(rst)
            time.sleep(0.2)

    @current_service.route("/", methods=['POST'])
    def input_blocks():
        received_block = request.get_json()
        check_blocks = current_node.get_input_block(received_block)
        if not check_blocks:
            return "block_handler_flag Error"
        return "We received new Block"

    current_server = threading.Thread(target=current_service.run, args=(host, port1))
    current_server_generator = threading.Thread(target=create_new_blocks)
    current_server.setDaemon(False)
    current_server_generator.setDaemon(False)
    current_server.start()
    current_server_generator.start()

    if service == 1:
        time.sleep(1)
        genesis = Block(1, 0, 'None')
        rs = (grequests.post(u, json=genesis.get_block_data()) for u in servers_urls)
        grequests.map(rs)
