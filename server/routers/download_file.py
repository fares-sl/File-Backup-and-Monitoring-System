from fastapi import APIRouter, HTTPException, status
from models.DownloadFile import DownloadFile
from fastapi.responses import FileResponse
from pathlib import Path
from database.db_services import cleanDownloadedPath
from services.exceptions_handlers import checkDownloadRequest, verifyCredentialsExistence


router = APIRouter()

@router.post('/api/download_file')
def downloadFile(downloadObject : DownloadFile):
    verifyCredentialsExistence(downloadObject.device_id, downloadObject.user)
    checkDownloadRequest(downloadObject.device_id, downloadObject.user, downloadObject.path)
    cleanDownloadedPath(downloadObject.device_id, downloadObject.user, downloadObject.path)
    return FileResponse(
        path = downloadObject.path,
        filename = Path(downloadObject.path).name,
        media_type = 'application/octet-stream'
    )
