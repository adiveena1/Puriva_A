import hashlib
import time
import json

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions = []

    def create_genesis_block(self):
        return Block(0, [], time.time(), "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, sender, recipient, amount):
        self.pending_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })

    def mine_block(self, miner_address):
        # Reward for mining (simplified, no real cryptocurrency economics)
        self.pending_transactions.append({
            "sender": "network",
            "recipient": miner_address,
            "amount": 10.0  # Mining reward
        })

        block = Block(len(self.chain), self.pending_transactions, time.time(), self.get_latest_block().hash)
        
        # Proof of Work: Find a nonce that produces a hash with required leading zeros
        while block.hash[:self.difficulty] != "0" * self.difficulty:
            block.nonce += 1
            block.hash = block.calculate_hash()

        print(f"Block mined! Nonce: {block.nonce}, Hash: {block.hash}")
        self.chain.append(block)
        self.pending_transactions = []

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # Verify current block's hash
            if current_block.hash != current_block.calculate_hash():
                print(f"Invalid hash in block {i}")
                return False

            # Verify chain continuity
            if current_block.previous_hash != previous_block.hash:
                print(f"Chain broken at block {i}")
                return False

        return True

# Example usage
if __name__ == "__main__":
    # Create a new blockchain
    mycoin = Blockchain(difficulty=4)

    # Add some transactions
    mycoin.add_transaction("Alice", "Bob", 50.0)
    mycoin.add_transaction("Bob", "Charlie", 30.0)

    # Mine a block
    print("Mining block 1...")
    mycoin.mine_block("Miner1")

    # Add more transactions
    mycoin.add_transaction("Charlie", "Alice", 20.0)
    mycoin.add_transaction("Bob", "Dave", 10.0)

    # Mine another block
    print("Mining block 2...")
    mycoin.mine_block("Miner2")

    # Verify the chain
    print("Is blockchain valid?", mycoin.is_chain_valid())

    # Print the blockchain
    for block in mycoin.chain:
        print(f"Block #{block.index}:")
        print(f"  Timestamp: {block.timestamp}")
        print(f"  Transactions: {block.transactions}")
        print(f"  Previous Hash: {block.previous_hash}")
        print(f"  Hash: {block.hash}")
        print(f"  Nonce: {block.nonce}\n")