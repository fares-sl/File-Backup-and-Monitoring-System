from pydantic import BaseModel

class UserConfig(BaseModel):
    roots : list[str]
    extensions : list[str]
    period : int
    paths : list[str]
    paths_to_download : list[str]