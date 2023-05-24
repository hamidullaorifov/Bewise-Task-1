import os
from sqlalchemy import create_engine,Column,Integer,DateTime,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime


POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')


SQLALCHEMY_DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db/{POSTGRES_DB}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)


Base = declarative_base()
Session = sessionmaker(bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer,primary_key=True)
    question_text = Column(String)
    answer_text = Column(String)
    created_at = Column(DateTime,default=datetime.now)

    def __repr__(self) -> str:
        return f'Question {self.id}'
