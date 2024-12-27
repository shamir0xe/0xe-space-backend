from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MaskedPost(BaseModel):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    title: Optional[str] = None
    content: Optional[str] = None
    rating_avg: Optional[float] = None
