from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MaskedUser(BaseModel):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    username: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    is_admin: Optional[bool] = None
