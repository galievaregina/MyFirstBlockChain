import json
import random
import string
from hashlib import sha256


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
