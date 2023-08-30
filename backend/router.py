from fastapi import APIRouter, HTTPException, Path, Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schema import QuestionSchema,RequestQuestions, Response
import crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()

@router.post('/create')
async def create(request:RequestQuestions, db:Session=Depends(get_db)):
    crud.create_question(db, request.parameter)
    return Response(code=200, status="Ok",message="Book created successfully").dict(exclude_none=True)

@router.get('/db')
async def get(db: Session = Depends(get_db)):
    _questions = crud.get_questions(db, 0, 100)
    return Response(code=200, status="Ok", message="Success", result=_questions).dict(exclude_none=True)

@router.get("/get/{path}")
async def get_by_id(path: str, db: Session = Depends(get_db)):
    _questions = crud.get_questions_by_url(db, path)
    return Response(code=200, status="Ok", message="Success", result=_questions).dict(exclude_none=True)

@router.delete("/delete/{path}")
async def delete(id: str, db: Session = Depends(get_db)):
    crud.remove_questions(db, question_url=id)
    return Response(code=200, status="Ok", message="Success").dict(exclude_none=True)


