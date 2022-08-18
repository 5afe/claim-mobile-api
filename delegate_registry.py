import os
import json
from hexbytes import HexBytes
from web3 import Web3
from web3.types import Address
from web3.providers import HTTPProvider


# https://github.com/gnosis/delegate-registry/blob/main/contracts/DelegateRegistry.sol
DELEGATE_REGISTRY_ADDRESS = HexBytes("0x469788fe6e9e9681c6ebf3bf78e7fd26fc015446")
DELEGATE_ID = "safe.eth"


INFURA_PROJECT_ID = os.environ.get('INFURA_PROJECT_ID')
w3 = Web3(HTTPProvider(f"https://rinkeby.infura.io/v3/{INFURA_PROJECT_ID}"))


def get_delegate(delegator_address):
    with open('assets/abi/DelegateRegistry.json') as abi_file:
        abi = json.load(abi_file)
        contract = w3.eth.contract(address=Address(DELEGATE_REGISTRY_ADDRESS), abi=abi)

        delegate = contract.functions.delegation(Address(delegator_address), DELEGATE_ID.encode('utf-8')).call()

        print(delegate)

        return delegate
