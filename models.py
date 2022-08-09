import database as _database
import sqlalchemy as _sqlalchemy
import datetime as _datetime


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
