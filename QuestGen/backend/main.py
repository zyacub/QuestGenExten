from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from config import engine
import logging
import router
from newspaper import Article
from string import punctuation
from heapq import nlargest
from pprint import pprint
from tqdm.auto import tqdm
from haystack.nodes import QuestionGenerator
from haystack.pipelines import (
    QuestionGenerationPipeline,
    QuestionAnswerGenerationPipeline,
)
from haystack.nodes import QuestionGenerator

import os
from dotenv import load_dotenv
logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
logging.getLogger("haystack").setLevel(logging.INFO)

models.Base.metadata.create_all(bind=engine)

question_generator = QuestionGenerator()


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return "Hello! Use the following syntax: /url/'url path'"

@app.get("/url/{full_path:path}")
async def url(full_path: str):
    print("generating questions")
    questions = generate_questions(full_path)
    print(questions)
    return questions

app.include_router(router.router, prefix="/questions", tags=["questions"])

def get_text(url): #Uses the newspaper3k library to get the main text from a website
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    text = article.text
    return text

def generate_questions(url):
    text = get_text(url) 
    question_list = question_generator.generate(text)
    pprint(question_list)
    return question_list
