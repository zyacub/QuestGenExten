from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from newspaper import Article

import openai

import ast

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
from dotenv import load_dotenv
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAIKEY")


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

llm = OpenAI(model_name="gpt-3.5-turbo")

question = "How do helicopters fly"
#Chain to generate questions
question_template = """Given the raw data from a website, generate a list of 10 questions that can be used to quiz someone on the information present in the website.
 For each question, include a label "source" that has a direct quote from the website that can indicate where the answer can be found. 
 Make sure "source" is a direct quotation directly from the text.  Have your questions build on one another and be in order of which the text appears on the page:

 Data: {data}
 These are the 10 questions:"""

prompt_template = PromptTemplate(input_variables=["data"], template=question_template)
question_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="questions")

#Chain to reformat into a dict
format_template = """Given the following data of questions and corresponding sources, reformat it into a list of two lists in the following format. Make sure each item in the two lists are valid python strings. Only include the questions for the first list, and sources in the second list. Make sure you include every question. Copy this format:
  [[question1, question2, question3, question4, question5, question6, question7, question8, question9, question10], [source 1, source 2, source 3, source 4, source 5, source 6, source 7, source 8, source 9, source 10]]

  Data: {questions}
  This is the list:"""

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
    #web_loader = WebBaseLoader(url)
    data = get_text(url)
    result = overall_chain.run({"data":data})
    pprint(result)
    #result = question_chain.run({"data": data[0].page_content})
    result = ast.literal_eval(result)
    return result