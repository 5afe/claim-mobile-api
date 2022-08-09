import pydantic as _pydantic
import datetime as _datetime


class Guardian(_pydantic.BaseModel):
    address: str
    ens: str
    name: str
    image_url: str
    reason: str
    contribution: str
    start_date: _datetime.datetime

    class Config:
        orm_mode = True  # stop lazy loading of the data


class Allocation(_pydantic.BaseModel):
    user: str
    ecosystem: str
    last_claim: str

    class Config:
        orm_mode = True  # stop lazy loading of the data
