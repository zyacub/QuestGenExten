from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import openai

from langchain.document_loaders import WebBaseLoader
from langchain.prompts.prompt import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

import models
from config import engine
import logging
import router
from pprint import pprint
from tqdm.auto import tqdm

import os
os.environ['OPENAI_API_KEY'] = "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"


models.Base.metadata.create_all(bind=engine)


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


#Chain Defintions
from langchain.prompts.prompt import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain

llm = OpenAI(temperature=.7)
#Chain to generate questions
question_template = """Given the raw data from a website, generate a list of 10 questions that can be used to quiz someone on the information present in the website.
 For each question, include a label "source" that has a direct quote from the website that can indicate where the answer can be found. 
 Make sure "source" is a direct quotation directly from the text.  Have your questions build on one another and be in order of which the text appears on the page:

 Data: {data}
 These are the 10 questions:"""

prompt_template = PromptTemplate(input_variables=["data"], template=question_template)
question_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="questions")

#Chain to reformat into a dict
format_template = """Given the following data of questions and corresponding sources, reformat it into a dictionary in the following format:
  1: [question: first_question, source: first_question source], 2: [question: second_question, source: second_question source]

  Data: {questions}
  This is the dictionary:"""

prompt_template = PromptTemplate(input_variables=["questions"], template=format_template)
reformat_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="question_dict")

#Combined Chain
overall_chain = SequentialChain(
    chains=[question_chain, reformat_chain],
    input_variables=["data"],
    output_variables=["question_dict"],
    verbose=True
)


def generate_questions(url):
    web_loader = WebBaseLoader(url)
    data = web_loader.load()
    result = overall_chain.run({"data":data[0].page_content})
    return result

    