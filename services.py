import models as _models
import sqlalchemy.orm as _orm
import dtos as _dtos
import database as _database


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
        dto.image_url = f"{url}/{guardian.address}/image"
        return dto
    return map_guardian
