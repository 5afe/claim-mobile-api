import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm
import schemas as _schemas
import services as _services
import schemas as _schemas
from typing import List

from fastapi.responses import FileResponse
from fastapi import Request, Query

app = _fastapi.FastAPI()


@app.get("/api/v1/guardians", response_model=List[_schemas.Guardian])
async def guardians(
        request: Request,
        db: _orm.Session = _fastapi.Depends(_services.get_db),

):
    return await _services.get_guardians(request.url._url, db=db)


@app.get("/api/v1/guardians/{address}", response_model=_schemas.Guardian)
async def guardian(
        address,
        db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    guardian = await _services.get_guardian_by_address(address=address, db=db)
    if guardian:
        raise _fastapi.HTTPException(status_code=404, detail="guardian not found")


class ImageParams:
    def __init__(
        self,
        size: str = Query(..., description="Image size")
    ):
        self.size = size


@app.get("/api/v1/guardians/{address}/image", response_class=FileResponse)
async def guardian_image(address, size="1x", params: ImageParams = _fastapi.Depends()):
    return FileResponse(f"images/{address}_{size}.jpg")


@app.get("/api/v1/{address}/delegate", response_model=str)
async def get_delegate(
        address,
        db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    pass


@app.get("/api/v1/{address}/allocation", response_model=_schemas.Allocation)
async def allocation(
        address,
        db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    pass


@app.get("/api/v1/{address}/check", response_model=bool)
async def claim_check(
        address,
        db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    pass