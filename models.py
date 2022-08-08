import datetime as _datetime
import sqlalchemy
import sqlalchemy as _sqlalchemy
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import db as _database


class GuardianModel(_database.Base):

    __tablename__ = "guardians"

    address = _sqlalchemy.Column(_sqlalchemy.String, primary_key=True, index=True)
    name = _sqlalchemy.Column(_sqlalchemy.String)
    ens = _sqlalchemy.Column(_sqlalchemy.String)
    image_url = _sqlalchemy.Column(_sqlalchemy.String)
    reason = _sqlalchemy.Column(_sqlalchemy.TEXT)
    contribution = _sqlalchemy.Column(_sqlalchemy.TEXT)
    start_date = _sqlalchemy.Column(_sqlalchemy.DateTime, default=_datetime.datetime.utcnow())
    submit_date = _sqlalchemy.Column(_sqlalchemy.DateTime, default=_datetime.datetime.utcnow())


class GuardianImageModel(_database.Base):

    __tablename__ = "guardian_images"

    guardian_address = _sqlalchemy.Column(
        _sqlalchemy.String,
        _sqlalchemy.ForeignKey("guardians.address"),
        primary_key=True,
        index=True
    )
    img_1x = _sqlalchemy.Column(_sqlalchemy.BLOB)
    img_2x = _sqlalchemy.Column(_sqlalchemy.BLOB)
    img_3x = _sqlalchemy.Column(_sqlalchemy.BLOB)

