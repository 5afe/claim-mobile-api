import pydantic as _pydantic
import datetime as _datetime
from typing import Optional


class Guardian(_pydantic.BaseModel):
    address: str
    ens: Optional[str]
    name: str
    imageUrl: str
    reason: str
    contribution: str

    class Config:
        orm_mode = True  # stop lazy loading of the data


class Vesting(_pydantic.BaseModel):
    id: str
    account: str
    curveType: int
    durationWeeks: int
    startDate: int
    amount: str
    proof: list


class Allocation(_pydantic.BaseModel):
    userVesting: Optional[Vesting]
    ecosystemVesting: Optional[Vesting]
