from audioop import add
from dis import Bytecode
import json
from solcx import compile_standard, install_solc
from web3 import Web3
import os
from dotenv import load_dotenv

### This code work with infura ###

load_dotenv()

with open("./simpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)


# Compile our solidity
print("installing solidity compiler")
install_solc("0.6.12")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.12",
)
# print(compiled_sol)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]

# print(abi)

w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/e5e131833bae477bbd3cdf347477b87f")
)
chian_id = 4
my_adress = "0x91aeF53c25f6056A09d750cB726C6CAD77D14e7b"
private_key = os.getenv("PRIVATE_KEY")
# os.getenv("PRIVATE_KEY")

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_adress)
print("nonce:{}".format(nonce))

transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chian_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_adress,
        "nonce": nonce,
    }
)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# print(signed_txn)

print("-> Deploying contract...")
# Send this signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")

# Contract address
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Call -> Simulate making the call and getting a return value
# Transact -> Actually make a state change
##print(simple_storage.functions.retrieve().call())
##print(simple_storage.functions.store(15).call()) # -> simulation
##print(simple_storage.functions.retrieve().call())

# Initial favorite number
# CREATE
print("Store() of simpleStorage called...")
print("store:{}".format(simple_storage.functions.retrieve().call()))
print("-> Contract...")
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chian_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_adress,
        "nonce": nonce + 1,
    }
)
# SIGNED
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
# SEND
signed_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
# WAIT TRANSACTION TO FINISH
tx_receipt = w3.eth.wait_for_transaction_receipt(signed_store_tx)
print("Updated!")

# print(simple_storage.functions.retrieve().call())
print("Store() of simpleStorage called...")
print("store:{}".format(simple_storage.functions.retrieve().call()))

# export PRIVATE_KEY=78d4771d19723948e5f5e55536b49a18ec1af245e01e31a690823e40fbd9a40d
# echo $PRIVATE_KEY
