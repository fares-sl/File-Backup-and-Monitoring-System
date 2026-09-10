from fastapi import APIRouter
from models.UserRegister import UserRegister
from database.db_services import registerUser

router = APIRouter()

@router.post("/api/register_user")

def register_user(user : UserRegister):
    registerUser(user.device_id, user.user, user.watched_roots, user.watched_extensions, user.period)
