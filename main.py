from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Initialize FastAPI
app = FastAPI()

# Initialize SQLAlchemy
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define a database model
class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, index=True)
    content = Column(String)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Pydantic model for input data
class MessageIn(BaseModel):
    id: str
    content: str

# PUT endpoint to store messages in the database
@app.put("/messages/")
def create_message(message: MessageIn):
    db = SessionLocal()
    db_message = Message(id=message.id, content=message.content)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

# GET endpoint to retrieve messages from the database
@app.get("/messages/{message_id}")
def get_message(message_id: str):
    db = SessionLocal()
    message = db.query(Message).filter(Message.id == message_id).first()
    if message:
        return message
    else:
        return {"error": "Message not found"}

# Root endpoint
@app.get("/")
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to FastAPI!"}

# Previous sim_test endpoint modified to use GET
@app.get('/sim_test')
def sim_test(id: str = None):
    if id:
        return {id}
    else:
        return {"Hello world"}
