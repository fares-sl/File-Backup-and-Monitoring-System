from fastapi import FastAPI
from routers.actions import router as actions_router
from routers.register import router as register_router
from routers.upload import router as upload_router
from routers.register_user import router as register_user_router
from routers.download_file import router as download_file_router

app = FastAPI()

app.include_router(actions_router)
app.include_router(register_router)
app.include_router(upload_router)
app.include_router(register_user_router)
app.include_router(download_file_router)

@app.get("/")
def root():
    return {"message": "Server is running"}