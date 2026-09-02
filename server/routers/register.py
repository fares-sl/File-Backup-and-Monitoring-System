from fastapi import APIRouter
from db_services import generateAgentId
from models.AgentRegister import AgentRegister

router = APIRouter()

@router.post('/api/register')

def register_agent(registerObject : AgentRegister) :
    return {"agent_id": generateAgentId(registerObject.hostName)}
