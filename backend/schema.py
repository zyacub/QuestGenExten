from typing import Optional, Generic, TypeVar, List
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar('T')

class QuestionSchema(BaseModel):
    url: Optional[str]=None
    data: Optional[List]=None

    class Config:
        orm_mode = True

class RequestQuestions(BaseModel):
    parameter: QuestionSchema = Field(...)

class DataSchema(BaseModel):
    url: Optional[str]=None
    questions: Optional[List]=None
    helpful: Optional[List]=None

    class Config:
        orm_mode = True

class RequestData(BaseModel):
    parameter: DataSchema = Field(...)   

class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]