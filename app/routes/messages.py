from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.message import Message
from app.schemas.message import MessageCreate
import uuid

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/messages")
def create_message(msg: MessageCreate, db: Session = Depends(get_db)):
    try:
        new_message = Message(
            id=str(uuid.uuid4()),
            recipient_id=msg.recipient_id,
            sender_name=msg.sender_name,
            sender_email=msg.sender_email,
            project_scope=msg.project_scope,
            message=msg.message,
        )
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        return {"message": "Message sent successfully", "id": new_message.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.get("/messages/{recipient_id}")
def get_messages(recipient_id: str, db: Session = Depends(get_db)):
    messages = (
        db.query(Message)
        .filter(Message.recipient_id == recipient_id)
        .order_by(Message.created_at.desc())
        .all()
    )
    return messages
