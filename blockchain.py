import time
import hashlib
import json
from flask import Flask, jsonify, request, render_template, redirect, url_for
import requests
from uuid import uuid4
from urllib.parse import urlparse

class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof=1, previous_hash='0')
        self.nodes = set()

    def add_node(self, address):
        self.nodes.add(address)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            try:
                response = requests.get(f"http://127.0.0.1:{node}/chain")
                if response.status_code == 200:
                    response = response.json()
                    length = response['length']
                    chain = response['chain']
                    if length > max_length and self.is_chain_valid(chain):
                        max_length = length
                        longest_chain = chain
                    if longest_chain is not None:
                        self.chain = longest_chain
                        return True
            except:
                pass
        return False


    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(time.time()),
            'transactions': self.transactions,
            'proof': proof,
            'previous_hash':previous_hash
        }
        self.transactions = []
        self.chain.append(block)
        return block
    
    def add_transaction(self, sender, recipient, amount):
        transaction = ({"sender":sender,
                        "recipient":recipient,
                        "amount":amount})
        self.transactions.append(transaction)
        previous_block = self.get_previous_block()
        return previous_block['index']+1

    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is not True:
            hash = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash[:4] == '4242':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        hash = hashlib.sha256(encoded_block).hexdigest()
        return hash
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash[:4] != '4242':
                return False
            previous_block = block
            block_index += 1
        return True