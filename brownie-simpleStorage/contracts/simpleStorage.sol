// SPDX-License-Identifier: MIT

pragma solidity 0.8.11;

// Class
contract SimpleStorage {
    // This wiil get initialize to 0!
    uint256 favoriteNumber;

    struct People {
        uint256 favoriteNumber;
        string name;
    }

    People[] public people;
    mapping(string => uint256) public nameToFavoriteNumeber;

    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    // view, pure -> reading of blockchain
    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    // memory -> during the function
    // storage -> on the contract
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People({favoriteNumber: _favoriteNumber, name: _name}));
        nameToFavoriteNumeber[_name] = _favoriteNumber;
    }
}
