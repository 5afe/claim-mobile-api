import db as _database
import models as _models
import sqlalchemy.orm as _orm
import schemas as _schemas


def create_db():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_guardian_by_address(address: str, db: _orm.Session):
    return db.query(_models.GuardianModel).filter(_models.GuardianModel.address == address).first()


async def get_guardians(url, db: _orm.Session):
    guardians = db.query(_models.GuardianModel)
    #return list(map(_schemas.Guardian.from_orm, guardians))
    return list(map(map_guardian_with_url(url), guardians))


def map_guardian_with_url(url):
    def map_guardian(guardian):
        dto = _schemas.Guardian.from_orm(guardian)
        dto.image_url = f"{url}/{guardian.address}/image"
        return dto
    return map_guardian


create_db()

