from sqlalchemy import Column, Integer, String, Float, Text, TIMESTAMP
from database import Base

class TelegramMessage(Base):
    __tablename__ = "telegram_messages"

    id = Column(Integer, primary_key=True, index=True)
    channel_title = Column(Text, nullable=False)
    channel_username = Column(Text, nullable=False)
    message_id = Column(Integer, unique=True, nullable=False)
    message = Column(Text, nullable=True)
    message_date = Column(TIMESTAMP, nullable=True)
    media_path = Column(Text, nullable=True)
    emoji_used = Column(Text, nullable=True)
    youtube_links = Column(Text, nullable=True)

class DetectedObject(Base):
    __tablename__ = "detected_objects"

    id = Column(Integer, primary_key=True, index=True)
    image_name = Column(String, nullable=False)
    class_id = Column(Integer, nullable=False)
    x_center = Column(Float, nullable=False)
    y_center = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)
    detection_timestamp = Column(TIMESTAMP, default=None)
