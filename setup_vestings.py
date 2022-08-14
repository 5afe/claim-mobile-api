import sqlalchemy.orm as _orm
import models as _models
import csv
import datetime
import os
from hexbytes import HexBytes
from eth_abi import abi, encode
from eth_typing import ChecksumAddress, HexStr
from eth_utils import function_abi_to_4byte_selector
from eth_abi.packed import encode_packed
import web3
from web3 import Web3
from web3._utils.encoding import pad_bytes, to_bytes
from web3._utils.abi import get_abi_input_names, get_abi_input_types, map_abi_data
from web3._utils.normalizers import BASE_RETURN_NORMALIZERS
from web3.contract import Contract
from web3.types import ABIFunction
from web3.providers import HTTPProvider
import merkle_proof

USER_AIRDROP_ADDRESS = HexBytes("0x6C6ea0B60873255bb670F838b03db9d9a8f045c4")
ECOSYSTEM_AIRDROP_ADDRESS = HexBytes("0x82F1267759e9Bea202a46f8FC04704b6A5E2Af77")

VESTING_ROOT = "0x998b43f028dc3dc6a3d5bb7f7828d092025dc09164ee400f1e0e52064466c67d"
VESTING_TYPEHASH = HexBytes("0x43838b5ce9ca440d1ac21b07179a1fdd88aa2175e5ea103f6e37aa6d18ce78ad")
DOMAIN_SEPARATOR_TYPEHASH = HexBytes("0x47e79534a245952e8b16893a336b85a3d9ea9fa8c573f3d803afb92a79469218")

INFURA_PROJECT_ID = os.environ.get('INFURA_PROJECT_ID')
w3 = Web3(HTTPProvider(f"https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}"))


class Vesting:
    def __init__(self, account, curveType, managed, durationWeeks, startDate, amount):
        self.account = account
        self.curveType = curveType
        self.managed = managed
        self.durationWeeks = durationWeeks
        self.startDate = startDate
        self.amount = amount


def calculate_vesting_hash(airdrop_address, vesting, chain_id):
    domainSeparator = Web3.solidityKeccak(
        ['bytes'],
        [
            abi.encode(
                ('bytes32', 'uint256', 'address'),
                (bytes(DOMAIN_SEPARATOR_TYPEHASH), chain_id, airdrop_address.hex())
            )
        ]
    )

    vestingDataHash = Web3.solidityKeccak(
        ['bytes'],
        [
            abi.encode(
                ('bytes32', 'address', 'uint8', 'bool', 'uint16', 'uint64', 'uint128'),
                (bytes(VESTING_TYPEHASH), vesting.account, vesting.curveType, vesting.managed,
                 int(vesting.durationWeeks), int(vesting.startDate.timestamp()), int(vesting.amount))
            )
        ]
    )

    vestingId = Web3.solidityKeccak(
        ['bytes'],
        [
            encode_packed(
                ('bytes1', 'bytes1', 'bytes', 'bytes'),
                (HexBytes(0x19), HexBytes(0x01), domainSeparator, vestingDataHash)
            )
        ]
    )

    return HexBytes(vestingId).hex()


# type ['user' | 'ecosystem']
def parse_vestings_csv(db: _orm.Session, type):
    vesting_file: str

    if type == "user":
        vesting_file = 'assets/user_airdrop.csv'
    else:
        vesting_file = 'assets/ecosystem_airdrop.csv'

    with open(vesting_file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0

        print(80 * "-")
        print(f"Processing {type} vestings")
        print(80 * "-")

        for row in csv_reader:
            if line_count == 0:
                line_count += 1

            owner = row["owner"]
            duration_weeks = row["duration"]
            start_date = datetime.datetime.strptime(row["startDate"], "%Y-%m-%dT%H:%M:%S%z")
            amount = row["amount"]
            curve_type = 0
            managed = False

            vesting = Vesting(owner, curve_type, managed, duration_weeks, start_date, amount)
            vesting_id = calculate_vesting_hash(USER_AIRDROP_ADDRESS, vesting, 4) if type == "user" \
                else calculate_vesting_hash(ECOSYSTEM_AIRDROP_ADDRESS, vesting, 4)

            vesting_model = _models.VestingModel(
                vestingId=vesting_id,
                type=type,
                owner=owner,
                curveType=curve_type,
                durationWeeks=duration_weeks,
                startDate=start_date,
                amount=amount
            )

            db.add(vesting_model)
            db.commit()
            db.refresh(vesting_model)

            print(f"[{type}] {owner}: {vesting_id}")

            line_count += 1

        print(f'Processed {line_count} {type} vestings.')


def generate_and_add_proof(db: _orm.Session, type):

    vestings = db.query(_models.VestingModel).filter(_models.VestingModel.type == type)
    vestingIds = list(map(lambda vesting: vesting.vestingId, vestings))

    for vesting in vestings:

        proof, root = merkle_proof.generate(vestingIds, vesting.vestingId)

        proof_index = 0
        for part in proof:

            proof_model = _models.ProofModel(
                vestingId=vesting.vestingId,
                proof_index=proof_index,
                proof=part
            )

            db.add(proof_model)
            db.commit()
            db.refresh(proof_model)

            proof_index += 1
