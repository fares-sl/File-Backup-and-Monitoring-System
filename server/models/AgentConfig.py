from pydantic import BaseModel

class AgentConfig(BaseModel):
    roots : list[str]
    extensions : list[str]
    period : int
    paths : list[str]