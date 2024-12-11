from fastapi import FastAPI,Request, Form,HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
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


questions = [
    {
        "question": "What is the capital of France?",
        "options": ["A. Berlin", "B. Madrid", "C. Paris", "D. Rome"],
        "answer": "C"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["A. Earth", "B. Mars", "C. Jupiter", "D. Saturn"],
        "answer": "B"
    },
    {
        "question": "What is the largest mammal in the world?",
        "options": ["A. Elephant", "B. Blue Whale", "C. Giraffe", "D. Hippopotamus"],
        "answer": "B"
    },
    {
        "question": "Who wrote 'Romeo and Juliet'?",
        "options": ["A. Charles Dickens", "B. Jane Austen", "C. William Shakespeare", "D. Mark Twain"],
        "answer": "C"
    },
    {
        "question": "What is the chemical symbol for water?",
        "options": ["A. CO2", "B. H2O", "C. O2", "D. NaCl"],
        "answer": "B"
    }
]

# For rendering HTML templates
templates = Jinja2Templates(directory="templates")

# Route to serve the index page (similar to Flask's index.html)
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Route to return quiz questions (GET)
@app.get("/quiz")
async def get_questions():
    return JSONResponse(content=questions)

# Route to submit answers (POST)
@app.post("/submit")
async def submit_answers(answers: list[str]):
    correct_answers = 0
    wrong_answers = 0
    score = 0

    for user_answer, question in zip(answers, questions):
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