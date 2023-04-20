import random
import json
import time
import threading

from blockchain import Block, Node, start


def test_block_creatin():
    for i in range(20):
        block_index = random.randint(1, 100000)
        prev_hash = 'tests'
        service_id = random.randint(1, 3)
        new_block = Block(service_id, block_index, prev_hash)

        assert new_block is not None
        assert new_block.hash is not None
        assert new_block.data is not None
        assert new_block.index is not None
        assert new_block.service_id is not None
        assert new_block.prev_hash is not None
        assert new_block.nonce is not None
        assert new_block.index == block_index
        assert new_block.prev_hash == prev_hash
        assert new_block.index == block_index
        assert new_block.service_id == service_id
        assert new_block.hash[-4:] == "0000"
        assert len(new_block.data) == 256


def test_get_input_block():
    node1 = Node(1)
    input = json.dumps({
        'service_id': 1,
        'index': 0,
        'hash': 'test_hash',
        'prev_hash': 'prev_hash',
        'data': 'data',
        'nonce': 1
    })
    assert node1.get_input_block(input) is True


def test_start():
    node1 = Node(2)
    input = json.dumps({
        'service_id': 1,
        'index': 0,
        'hash': 'test_hash',
        'prev_hash': 'prev_hash',
        'data': 'data',
        'nonce': 1
    })
    assert node1.get_input_block(input) is True


