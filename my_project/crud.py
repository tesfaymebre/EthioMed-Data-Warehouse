from sqlalchemy.orm import Session
from models import TelegramMessage, DetectedObject
from schemas import TelegramMessageCreate, DetectedObjectCreate

# CRUD for TelegramMessage
def get_telegram_messages(db: Session, skip: int = 0, limit: int = 10):
    return db.query(TelegramMessage).offset(skip).limit(limit).all()

def create_telegram_message(db: Session, message: TelegramMessageCreate):
    db_message = TelegramMessage(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

# CRUD for DetectedObject
def get_detected_objects(db: Session, skip: int = 0, limit: int = 10):
    return db.query(DetectedObject).offset(skip).limit(limit).all()

def create_detected_object(db: Session, detected_object: DetectedObjectCreate):
    db_object = DetectedObject(**detected_object.dict())
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    return db_object
