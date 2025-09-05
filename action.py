from pydantic import BaseModel

class Action(BaseModel):
    tool_name: str
    description: str
    parameters: dict