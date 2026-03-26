#Blokları oluşturup zincire bağlanıyor. SHA-256 ile şifreleniyor

import time 
import hashlib


class Block:

  def __init__(self, index, data, previous_hash, proof):
    self.index = index
    self.data = data
    self.previous_hash = previous_hash
    self.proof = proof
    self.timestamp = time.time()
    self.hash = self.calculate_hash()

  def calculate_hash(self):
    hash_string = str(self.timestamp) + str(self.data) + str(self.previous_hash)
    return hashlib.sha256(hash_string.encode('utf-8')).hexdigest()
    

#Zincir oluşturuldu
class Blockchain:
  def __init__(self):
    self.chain = []
    self.chain.append(self.create_genesis_block())

  def create_genesis_block(self):
    return Block(0, "genesis block", "0", 100)
  
  def add_block(self, new_data):
    previous_block = self.chain[-1]
    new_index = previous_block.index + 1
    previous_hash = previous_block.hash
    previous_proof = previous_block.proof

    new_proof = self.proof_of_work(previous_proof, new_index, new_data)

    new_block = Block(new_index, new_data, previous_hash, new_proof)
    self.chain.append(new_block)
    return new_block

  def proof_of_work(self, previous_proof, index, data):
    proof = 0

    while self.valid_proof(proof, previous_proof, index, data) is False:
      proof += 1

    return proof

  def valid_proof(self, proof, previous_proof, index, data):
    guess = f"{proof**2 - previous_proof**2 + index}{data}". encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:4] == "0000"


  def is_chain_valid(self):
    for i in range(1, len(self.chain)):
      current_block = self.chain[i]
      previous_block = self.chain[i-1]
      if current_block.hash != current_block.calculate_hash():
        return False
      
      if current_block.previous_hash != previous_block.hash:
        return False
      
    return True

  def add_transaction(self, data):
    """Transaction eklemek için add_block'u kullan"""
    return self.add_block(data)
  
  
