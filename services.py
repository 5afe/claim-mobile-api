import models as _models
import sqlalchemy.orm as _orm
import dtos as _dtos
import database as _database
from datetime import datetime
import time
import merkle_proof
import vesting_status
import delegate_registry


def get_db():
    return next(_database.get_db())


async def get_guardian_by_address(url: str, address: str, db: _orm.Session):
    guardian = db.query(_models.GuardianModel).filter(_models.GuardianModel.address == address).first()
    if guardian:
        guardian = map_guardian_with_url(url)(guardian)
    return guardian


async def get_guardians(url, db: _orm.Session):
    guardians = db.query(_models.GuardianModel)
    return list(map(map_guardian_with_url(url), guardians))


def map_guardian_with_url(url):
    def map_guardian(guardian):
        dto = _dtos.Guardian.from_orm(guardian)
        if guardian.imageUrl:
            dto.imageUrl = f"{url}/{guardian.address}/image"
        return dto
    return map_guardian


async def get_allocation_by_address(address: str, db: _orm.Session):

    user_vesting = db.query(_models.VestingModel)\
        .filter(_models.VestingModel.owner == address, _models.VestingModel.type == "user")\
        .first()

    ecosystem_vesting = db.query(_models.VestingModel)\
        .filter(_models.VestingModel.owner == address, _models.VestingModel.type == "ecosystem")\
        .first()

    if user_vesting or ecosystem_vesting:

        userVesting: _dtos.Vesting = None
        ecosystemVesting: _dtos.Vesting = None

        if user_vesting:

            user_vestings = db.query(_models.VestingModel).filter(_models.VestingModel.type == "user")
            user_vesting_ids = list(map(lambda vesting: vesting.vestingId, user_vestings))
            user_vesting_proof, _ = merkle_proof.generate(user_vesting_ids, user_vesting.vestingId)

            userVesting = _dtos.Vesting(
                id=user_vesting.vestingId,
                account=user_vesting.owner,
                curveType=user_vesting.curveType,
                durationWeeks=user_vesting.durationWeeks,
                startDate=time.mktime(datetime.timetuple(user_vesting.startDate)),
                amount=user_vesting.amount,
                proof=user_vesting_proof
            )

        if ecosystem_vesting:

            ecosystem_vestings = db.query(_models.VestingModel).filter(_models.VestingModel.type == "ecosystem")
            ecosystem_vesting_ids = list(map(lambda vesting: vesting.vestingId, ecosystem_vestings))
            ecosystem_vesting_proof, _ = merkle_proof.generate(ecosystem_vesting_ids, ecosystem_vesting.vestingId)

            ecosystemVesting = _dtos.Vesting(
                id=ecosystem_vesting.vestingId,
                account=ecosystem_vesting.owner,
                curveType=ecosystem_vesting.curveType,
                durationWeeks=ecosystem_vesting.durationWeeks,
                startDate=time.mktime(datetime.timetuple(ecosystem_vesting.startDate)),
                amount=ecosystem_vesting.amount,
                proof=ecosystem_vesting_proof
            )

        allocationDto = _dtos.Allocation(
            userVesting=userVesting,
            ecosystemVesting=ecosystemVesting
        )

        return allocationDto


async def get_allocation_status_by_address(address: str, db: _orm.Session):

    user_vesting = db.query(_models.VestingModel) \
        .filter(_models.VestingModel.owner == address, _models.VestingModel.type == "user") \
        .first()

    ecosystem_vesting = db.query(_models.VestingModel) \
        .filter(_models.VestingModel.owner == address, _models.VestingModel.type == "ecosystem") \
        .first()

    if user_vesting or ecosystem_vesting:

        userVestingStatus: _dtos.VestingStatus = None
        ecosystemVestingStatus: _dtos.VestingStatus = None

        if user_vesting:
            userVestingStatus = vesting_status.get_user_vesting_status(user_vesting.vestingId)

        if ecosystem_vesting:
            ecosystemVestingStatus = vesting_status.get_ecosystem_vesting_status(ecosystem_vesting.vestingId)

        allocationStatusDto = _dtos.AllocationStatus(
            userVesting=userVestingStatus,
            ecosystemVesting=ecosystemVestingStatus,
        )

        return allocationStatusDto


async def get_delegate_for_address(url: str, address: str, db: _orm.Session):

    delegate_address = delegate_registry.get_delegate(address)

    if delegate_address != "0x0000000000000000000000000000000000000000":
        guardian = db.query(_models.GuardianModel).filter(_models.GuardianModel.address == delegate_address).first()
        if guardian:
            guardian = map_guardian_with_url(url)(guardian)
        else:
            guardian = _dtos.Guardian(address=delegate_address)
        return guardian
