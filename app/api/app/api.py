from fastapi import APIRouter, File, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse

from app.base.deta_base import db
from app.base.deta_drive import drive
from app.core.image.service import mergeImage
from app.schemas.response.common import RestfulResponse
from app.utils.time_layout import getFilePrefix

router = APIRouter()


@router.post("/add_record", response_model=RestfulResponse, include_in_schema=False)
def add_record(key: str, value: str) -> RestfulResponse:
    db.put(value, key=key, expire_in=300)
    return RestfulResponse(data={})


@router.post("/get_record", response_model=RestfulResponse, include_in_schema=False)
def get_record(key: str) -> RestfulResponse:
    ret = db.get(key)
    return RestfulResponse(data={"key": key, "value": ret})


@router.post("/upload", response_model=RestfulResponse)
def upload_img(file: UploadFile = File(...)) -> RestfulResponse:
    f = file.file
    ret = mergeImage(f.read())
    return RestfulResponse(data={"base64": ret})


@router.get("/download/{name}", include_in_schema=False)
def download_img(name: str):
    res = drive.get(name)
    return StreamingResponse(res.iter_chunks(1024), media_type="image/png")  # type: ignore
