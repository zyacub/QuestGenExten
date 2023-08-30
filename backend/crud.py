from sqlalchemy.orm import Session
from models import Questions
from schema import QuestionSchema

def get_questions(db:Session, skip:int=0,limit:int=100):
    return db.query(Questions).offset(skip).limit(limit).all()

def get_questions_by_url(db:Session, question_url: str):
    print(question_url)
    return db.query(Questions).filter(Questions.url == question_url).first()

def create_question(db:Session, questions: QuestionSchema):
    _questions = Questions(url=questions.url, data=questions.data)
    db.add(_questions)
    db.commit()
    db.refresh(_questions)
    return _questions

def remove_questions(db:Session, question_url:str):
    _questions = get_questions_by_url(db=db,question_url=question_url)
    db.delete(_questions)
    db.commit()


