from pydantic import BaseModel
from typing import Optional


class PackageCreate(BaseModel):
    tracking_number: str
    carrier_code: str
    nickname: Optional[str] = None


class PackageResponse(BaseModel):
    id: int
    user_id: int
    tracking_number: str
    carrier_code: str
    nickname: Optional[str] = None
    status_data: Optional[dict] = None

    class Config:
        from_attributes = True
