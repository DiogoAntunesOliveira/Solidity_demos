from brownie import FundMe, MockV3Aggregator, network, config, web3
from scripts.helpful_scripts import get_account
from web3 import Web3


def deploy_fund_me():
    account = get_account()

    if network.show_active() != "development":
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        print(f"The active network is {network.show_active()}")
        print("Deploying Mocks...")

        if len(MockV3Aggregator) <= 0:
            MockV3Aggregator.deploy(18, web3.toWei(200, "ether"), {"from": account})

        price_feed_address = MockV3Aggregator[-1].address
        print("Mocks Deployed!")

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")


def main():
    deploy_fund_me()
