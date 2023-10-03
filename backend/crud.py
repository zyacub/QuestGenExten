from sqlalchemy.orm import Session
from models import Questions, Data
from schema import QuestionSchema, DataSchema

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

#Data crud
def get_data(db:Session, skip:int=0,limit:int=100):
    return db.query(Data).offset(skip).limit(limit).all()

def get_data_by_url(db:Session, question_url: str):
    print(question_url)
    return db.query(Data).filter(Data.url == question_url).first()

def create_data(db:Session, data: DataSchema):
    _data = Data(url=data.url, questions=data.questions, helpful=data.helpful)
    db.add(_data)
    db.commit()
    db.refresh(_data)
    return _data

def remove_data(db:Session, question_url:str):
    _data = get_data_by_url(db=db,question_url=question_url)
    db.delete(_data)
    db.commit()




