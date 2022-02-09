from fnmatch import translate
from brownie import accounts, config, SimpleStorage, network
import os


def deploy_simple_storage():
    # account = accounts.load("dotchain-account")

    # Go to yaml file and search fro from_key and return .env key with ${PRIVATE_KEY}
    # account = accounts.add(config["wallets"]["from_key"])
    # account = accounts[0]
    account = get_account()

    # Deploy
    simple_storage = SimpleStorage.deploy({"from": account})

    # Call the value
    stored_value = simple_storage.retrieve()

    # Save on smart contract
    transaction = simple_storage.store(15, {"from": account}, publish_source=True)
    transaction.wait(1)

    # Call the value
    updated_stored_value = simple_storage.retrieve()

    print("stored_value:{}".format(stored_value))
    print("updated_stored_valuee:{}".format(updated_stored_value))


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()
