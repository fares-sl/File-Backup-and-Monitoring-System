from database.db_services import userExists
from fastapi import HTTPException, status
from database.db_services import DownloadRequestExists


def verifyCredentialsExistence(device_id, user):
    if not userExists(device_id, user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error: No such user found."
        )

def checkDownloadRequest(device_id, user, path):
    if not DownloadRequestExists(device_id, user, path):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error: Download request denied as admin permission not given."
        )
