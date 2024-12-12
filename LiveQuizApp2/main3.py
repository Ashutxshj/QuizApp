import asyncio
from fastapi import FastAPI,Request,Form,HTTPException, Request,Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List
import firebase_admin
from firebase_admin import credentials,auth,firestore
import openai
import os
import json
app = FastAPI()

app.mount("/static",StaticFiles(directory="static"),name="static")
templates=Jinja2Templates(directory="templates")
conn = MongoClient("mongodb+srv://Ashutosh:fuckmeup2004@cluster0.v5ypp.mongodb.net/quiz")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs =conn.Quiz.quiz.find({})
    for doc in docs:
        print(doc)
    return templates.TemplateResponse("index.html",{"request":request})

@app.get("/")
async def root():
    return {"message": "Hello"}

client = MongoClient("mongodb+srv://Ashutosh:fuckmeup2004@cluster0.v5ypp.mongodb.net/quiz")
db = client.Quiz
questions_collection = db.quiz

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/quiz")
async def get_questions():
# Fetch questions from MongoDB
    questions = list(questions_collection.find({}))
    # Convert MongoDB _id to string for JSON serialization
    for question in questions:
        question["_id"] = str(question["_id"])
    return JSONResponse(content=questions)

@app.post("/submit")
async def submit_answers(answers: list[str]):
    questions = list(questions_collection.find({}))
    for question in questions:
        question["_id"] = str(question["_id"])


    correct_answers = 0
    wrong_answers = 0
    score = 0

    for i, question in enumerate(questions):
        user_answer=await asyncio.wait_for(get_user_answer(i),timeout=30)

        if user_answer.upper() == question['answer']:
            correct_answers += 1
            score += 4
        else:
            wrong_answers += 1
            score -= 1

    result = {
        "total_questions": len(questions),
        "correct_answers": correct_answers,
        "wrong_answers": wrong_answers,
        "score": score
    }
    return JSONResponse(content=result)

class Question(BaseModel):
    question: str
    options: List[str]
    answer: str

class Quiz(BaseModel):
    questions: List[Question]

@app.post("/save-quiz")
async def save_quiz(quiz: Quiz):
    for question in quiz.questions:
        if len(question.options) != 4:
            raise HTTPException(status_code=400, detail="Each question must have exactly 4 options.")
        if question.answer not in ["A", "B", "C", "D"]:
            raise HTTPException(status_code=400, detail="Answer must be one of A, B, C, or D.")

    questions_collection.insert_many([q.dict() for q in quiz.questions])
    return {"message": "Quiz saved successfully!"}



#! Not-Working
API_KEY=open("key.txt","r").read().strip()
openai.api_key=API_KEY
class AIQuizRequest(BaseModel):
    topic:str
    num_questions: int=5

@app.post("/generate-ai-quiz")
async def generate_ai_quiz(request:AIQuizRequest):
    prompt=(
        f"Generate {request.num_questions} multiple-choice questions on the topic '{request.topic}'.\n"
        "Each question should have exactly four choices labeled A,B,C and D.Specify the correct answer.\n"
        "Return them in JSON format with the keys: 'question','options', and 'answer'."
    )

    try:
        response=openai.ChatCompletion.create(
            model="gpt-3.5-tubro",
            messages=[{
                "role":"user",
                "content":prompt
            }],
            max_tokens=1000,
            top_p=1,
            n=1,
            frequency_penalty=0,
            temperature=0.3
        )

        questions_text=response.choices[0].message.content
        print(questions)

        try:
            questions_list=json_loads(questions_text)
            if not isinstance(questions_list,list):
                raise ValueError("Invalid format returned from OpenAI.")
        except json.JSONDecodeError as e:
            print("Error parsing",e)
            raise HTTPException(status_code=500,detail="Failed to parse AI response.")
        
        for question in questions_list:
            questions_collection.insert_one(question)
        
        return {"message":"Quiz questions generated and saved successfully.","questions":questions_list}

    except openai.error.RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.")

    except openai.error.OpenAIError as e:
        print("OpenAI API Error:", e)
        raise HTTPException(status_code=500, detail="Failed to generate quiz questions.")