import pydantic as _pydantic
import datetime as _datetime


class Guardian(_pydantic.BaseModel):
    address: str
    ens: str
    name: str
    imageUrl: str
    reason: str
    contribution: str
    startDate: _datetime.datetime

    class Config:
        orm_mode = True  # stop lazy loading of the data


class Allocation(_pydantic.BaseModel):
    user: str
    ecosystem: str
    last_claim: str

    class Config:
        orm_mode = True  # stop lazy loading of the data
