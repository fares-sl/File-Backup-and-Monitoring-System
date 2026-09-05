from fastapi import APIRouter, UploadFile, File, Form
from services.action_services import concatenatePaths
import config

router = APIRouter()

@router.post('/api/upload')
async def upload_file(
    agent_id : int = Form(...),
    path : str = Form(...),
    file : UploadFile = File(...)
):
    data = await file.read()
    with open(concatenatePaths(config.BACKUP_ROOT, str(agent_id), path),'wb') as f:
        f.write(data)