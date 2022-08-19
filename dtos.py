import pydantic as _pydantic
import datetime as _datetime
from typing import Optional


class Guardian(_pydantic.BaseModel):
    address: str
    ens: Optional[str]
    name: Optional[str]
    imageUrl: Optional[str]
    reason: Optional[str]
    contribution: Optional[str]

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


class VestingStatus(_pydantic.BaseModel):
    isRedeemed: bool
    isPaused: bool
    amountClaimed: str


class AllocationStatus(_pydantic.BaseModel):
    userVesting: Optional[VestingStatus]
    ecosystemVesting: Optional[VestingStatus]
