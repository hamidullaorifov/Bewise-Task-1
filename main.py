import requests
from fastapi import FastAPI,Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db,Base,Question,engine

QUESTION_API_URL = 'https://jservice.io/api/random'
app = FastAPI()

Base.metadata.create_all(engine)




class QuestionRequest(BaseModel):
    questions_num: int



@app.post('/quiz')
def generate_quiz(request: QuestionRequest,db: Session = Depends(get_db)):
    number_questions = request.questions_num
    created_questions = create_unique_questions(number_questions,db)
    while number_questions != len(created_questions):
        created_questions+=create_unique_questions(number_questions-len(created_questions),db)
    print(created_questions)
    return created_questions
    

def create_unique_questions(questions_num,db):
    questions = get_questions(count=questions_num)
    new_questions = []
    for question in questions:
        if not db.query(Question).filter(Question.id==question['id']).first():
            new_question = save_question(question,db)
            new_questions.append(new_question)
    return new_questions


def get_questions(count=1):
    response = requests.get(QUESTION_API_URL,params={'count':count})
    return response.json()


def save_question(question_data,db):
    _id = question_data['id']
    question_text = question_data['question']
    answer_text = question_data['answer']
    new_question = Question(id=_id,question_text=question_text,answer_text=answer_text)
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question