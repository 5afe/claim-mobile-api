import fastapi as _fastapi
from fastapi.responses import FileResponse
from fastapi import Request, Query
import sqlalchemy.orm as _orm
import services as _services
import dtos as _dtos
from typing import List

description = """
Claim Mobile API for delivering guardian and vesting data. 🚀
"""



app = _fastapi.FastAPI(
    title="Claim Mobile API",
    description=description,
    version="0.0.1"
)


@app.get("/api/v1/guardians", response_model=List[_dtos.Guardian], response_model_exclude_none=True, tags=["Guardians"])
async def guardians(
        request: Request,
        db: _orm.Session = _fastapi.Depends(_services.get_db),

):
    return await _services.get_guardians(request.url._url, db=db)


@app.get("/api/v1/guardians/{address}", response_model=_dtos.Guardian, response_model_exclude_none=True, tags=["Guardians"])
async def guardian(
        request: Request,
        address,
        db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    url_parts = request.url._url.split("/")
    url_parts.remove(address)
    result = await _services.get_guardian_by_address("/".join(url_parts), address=address, db=db)

    if not result:
        raise _fastapi.HTTPException(status_code=404, detail="guardian not found")

    return result


class ImageParams:
    def __init__(
        self,
        size: str = Query("1x", description="Image size [ 1x, 2x, 3x ]")
    ):
        self.size = size


@app.get("/api/v1/guardians/{address}/image", response_class=FileResponse, tags=["Guardians"])
async def guardian_image(address, params: ImageParams = _fastapi.Depends()):
    return FileResponse(f"images/{address}_{params.size}.jpg")


# @app.get("/api/v1/{address}/delegate", response_model=str)
# async def get_delegate(
#         address,
#         db: _orm.Session = _fastapi.Depends(_services.get_db)
# ):
#     pass


@app.get("/api/v1/{address}/allocation", response_model=_dtos.Allocation,  response_model_exclude_none=True, tags=["Vestings"])
async def allocation(
        address,
        db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    result = await _services.get_allocation_by_address(address=address, db=db)

    if not result:
        raise _fastapi.HTTPException(status_code=404, detail="allocation not found")

    return result


# @app.get("/api/v1/{address}/check", response_model=bool)
# async def claim_check(
#         address,
#         db: _orm.Session = _fastapi.Depends(_services.get_db)
# ):
#     pass
