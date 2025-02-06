from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from schemas import TelegramMessageOut, TelegramMessageCreate, DetectedObjectOut, DetectedObjectCreate
import crud

# Initialize the app and create database tables
app = FastAPI(title="EthioMed Data Warehouse API")
Base.metadata.create_all(bind=engine)

# TelegramMessage Endpoints
@app.get("/telegram_messages", response_model=list[TelegramMessageOut])
def read_telegram_messages(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_telegram_messages(db, skip=skip, limit=limit)

@app.post("/telegram_messages", response_model=TelegramMessageOut)
def create_telegram_message(message: TelegramMessageCreate, db: Session = Depends(get_db)):
    return crud.create_telegram_message(db, message)

# DetectedObject Endpoints
@app.get("/detected_objects", response_model=list[DetectedObjectOut])
def read_detected_objects(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_detected_objects(db, skip=skip, limit=limit)

@app.post("/detected_objects", response_model=DetectedObjectOut)
def create_detected_object(detected_object: DetectedObjectCreate, db: Session = Depends(get_db)):
    return crud.create_detected_object(db, detected_object)
