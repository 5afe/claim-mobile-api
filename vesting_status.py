import os
import json
from dtos import VestingStatus
from hexbytes import HexBytes
from web3 import Web3
from web3.types import Address
from web3.providers import HTTPProvider


ZERO_ADDRESS = HexBytes("0x0000000000000000000000000000000000000000")
USER_AIRDROP_ADDRESS = HexBytes("0x6C6ea0B60873255bb670F838b03db9d9a8f045c4")
ECOSYSTEM_AIRDROP_ADDRESS = HexBytes("0x82F1267759e9Bea202a46f8FC04704b6A5E2Af77")

INFURA_PROJECT_ID = os.environ.get('INFURA_PROJECT_ID')
# w3 = Web3(HTTPProvider(f"https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}"))
w3 = Web3(HTTPProvider(f"https://rinkeby.infura.io/v3/{INFURA_PROJECT_ID}"))


def get_vesting_status(airdrop_address, vesting_id):
    with open('assets/abi/Airdrop.json') as abi_file:
        contract_interface = json.load(abi_file)
        contract = w3.eth.contract(address=Address(USER_AIRDROP_ADDRESS), abi=contract_interface['abi'])

        # https://github.com/safe-global/safe-token/blob/main/contracts/VestingPool.sol
        vesting_status = contract.functions.vestings(vesting_id).call()
        is_redeemed = False if (HexBytes(vesting_status[0]) == ZERO_ADDRESS) else True
        is_paused = vesting_status[7] != 0
        amount_claimed = vesting_status[6]

        vesting_status = VestingStatus(
            isRedeemed=is_redeemed,
            isPaused=is_paused,
            amountClaimed=amount_claimed
        )

        return vesting_status


def get_user_vesting_status(vesting_id):
    return get_vesting_status(USER_AIRDROP_ADDRESS, vesting_id)


def get_ecosystem_vesting_status(vesting_id):
    return get_vesting_status(ECOSYSTEM_AIRDROP_ADDRESS, vesting_id)
