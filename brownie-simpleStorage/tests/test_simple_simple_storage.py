from lib2to3.pgen2.literals import simple_escapes
from tracemalloc import start
from brownie import SimpleStorage, accounts


def test_deploy():
    # Arrange
    account = accounts[0]
    # Act
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()
    expected = 0
    # Assert
    assert starting_value == expected


# Test with pdb can debug
def test_updating_storage():
    # Arrange (setup)
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    # Act (test)
    excepted = 15
    simple_storage.store(excepted, {"from": account})
    # Assert (validation)
    assert excepted == simple_storage.retrieve()
