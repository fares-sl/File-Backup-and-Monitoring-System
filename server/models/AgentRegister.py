from pydantic import BaseModel

class AgentRegister(BaseModel):
    hostName : str

