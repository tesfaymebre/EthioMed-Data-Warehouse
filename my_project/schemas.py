from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema for TelegramMessage
class TelegramMessageBase(BaseModel):
    channel_title: str
    channel_username: str
    message_id: int
    message: Optional[str]
    message_date: Optional[datetime]
    media_path: Optional[str]
    emoji_used: Optional[str]
    youtube_links: Optional[str]

class TelegramMessageCreate(TelegramMessageBase):
    pass

class TelegramMessageOut(TelegramMessageBase):
    id: int

    class Config:
        orm_mode = True


# Schema for DetectedObject
class DetectedObjectBase(BaseModel):
    image_name: str
    class_id: int
    x_center: float
    y_center: float
    width: float
    height: float
    confidence: float
    detection_timestamp: Optional[datetime]

class DetectedObjectCreate(DetectedObjectBase):
    pass

class DetectedObjectOut(DetectedObjectBase):
    id: int

    class Config:
        orm_mode = True
