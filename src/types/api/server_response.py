from pydantic import BaseModel, Field


class ServerResponse(BaseModel):
    status: int = Field(default=200)
    message: str = Field(default="OK")
