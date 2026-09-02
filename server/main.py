from fastapi import FastAPI
from routers.actions import router as actions_router
from routers.register import router as register_router

app = FastAPI()

app.include_router(actions_router)
app.include_router(register_router)


@app.get("/")
def root():
    return {"message": "Server is running"}