import models as _models
import sqlalchemy.orm as _orm
import dtos as _dtos
import database as _database
import merkle_proof


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
                startDate=user_vesting.startDate,
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
                startDate=ecosystem_vesting.startDate,
                amount=ecosystem_vesting.amount,
                proof=ecosystem_vesting_proof
            )

        allocationDto = _dtos.Allocation(
            userVesting=userVesting,
            ecosystemVesting=ecosystemVesting
        )

        return allocationDto
