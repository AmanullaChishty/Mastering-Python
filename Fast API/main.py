from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String, index=True)
    description = Column(String)

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False,autocommit = False,bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ItemCreate(BaseModel):
    name:str
    description:str

class ItemRead(ItemCreate):
    id:int

@app.post("/item",response_model=ItemRead)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(name=item.name,description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
