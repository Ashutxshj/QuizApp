from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
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
    return {"message": "Fuck you"}