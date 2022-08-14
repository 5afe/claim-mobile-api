import database as _database
import sqlalchemy as _sqlalchemy
from sqlalchemy.orm import relationship
import datetime as _datetime


class GuardianModel(_database.Base):

    __tablename__ = "guardians"

    address = _sqlalchemy.Column(_sqlalchemy.String, primary_key=True, index=True)
    name = _sqlalchemy.Column(_sqlalchemy.String)
    ens = _sqlalchemy.Column(_sqlalchemy.String)
    imageUrl = _sqlalchemy.Column(_sqlalchemy.String)
    reason = _sqlalchemy.Column(_sqlalchemy.TEXT)
    contribution = _sqlalchemy.Column(_sqlalchemy.TEXT)
    startDate = _sqlalchemy.Column(_sqlalchemy.DateTime, default=_datetime.datetime.utcnow())
    submitDate = _sqlalchemy.Column(_sqlalchemy.DateTime, default=_datetime.datetime.utcnow())


class VestingModel(_database.Base):

    __tablename__ = "vestings"

    vestingId = _sqlalchemy.Column(_sqlalchemy.String, primary_key=True, index=True)
    type = _sqlalchemy.Column(_sqlalchemy.String)
    owner = _sqlalchemy.Column(_sqlalchemy.String)
    curveType = _sqlalchemy.Column(_sqlalchemy.Integer)
    durationWeeks = _sqlalchemy.Column(_sqlalchemy.Integer)
    startDate = _sqlalchemy.Column(_sqlalchemy.DateTime)
    amount = _sqlalchemy.Column(_sqlalchemy.String)

    # proofs = relationship("ProofModel",  backref="vestings")


# class ProofModel(_database.Base):
#
#     __tablename__ = "proofs"
#
#     vestingId = _sqlalchemy.Column(_sqlalchemy.String, _sqlalchemy.ForeignKey("vestings.vestingId"), primary_key=True, index=True)
#     proof_index = _sqlalchemy.Column(_sqlalchemy.Integer, primary_key=True)
#     proof = _sqlalchemy.Column(_sqlalchemy.String, primary_key=True)
