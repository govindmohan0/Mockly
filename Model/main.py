from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from gtts import gTTS
import whisper
import fitz
import os
from pymongo import MongoClient
from tempfile import NamedTemporaryFile
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from crew import question_crew, response_crew  
from fastapi.staticfiles import StaticFiles
import shutil

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.ai_interview
collection = db.transcripts

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResumeInput(BaseModel):
    data: str  

def extract_resume_text(pdf_file):
    doc = fitz.open(pdf_file)
    text = "".join(page.get_text() for page in doc)
    return text

@app.post("/upload_resume/")
async def upload_resume(file: UploadFile = File(...)):
    with NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    resume_text = extract_resume_text(temp_file_path)
    os.remove(temp_file_path)

    return {"parsed_data": resume_text}

@app.post("/generate_questions/")
async def generate_questions(resume_data: ResumeInput):
    if not resume_data.data:
        raise HTTPException(status_code=400, detail="Resume data is required")

    question = question_crew.kickoff(inputs={"data": resume_data.data})  # AI generates question

    # Ensure 'static/' directory exists
    os.makedirs("static", exist_ok=True)

    # Save MP3 file in the static folder
    audio_path = f"static/question_audio.mp3"
    gTTS(text=question, lang='en').save(audio_path)

    # Return URL pointing to static file
    return {"question": question, "audio_url": f"http://localhost:8000/static/question_audio.mp3"}

@app.post("/process_audio/")
async def process_audio(file: UploadFile = File(...), question: str = None, background_tasks: BackgroundTasks = None):
    model = whisper.load_model("base")
    with NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(await file.read())
        temp_audio_path = temp_audio.name

    transcription = model.transcribe(temp_audio_path)["text"]
    os.remove(temp_audio_path)

    evaluation = response_crew.kickoff(inputs={"data": transcription})
    feedback_audio_path = "feedback_audio.mp3"
    gTTS(text=evaluation, lang='en').save(feedback_audio_path)
    background_tasks.add_task(os.remove, feedback_audio_path)

    return JSONResponse(content={"transcription": transcription, "feedback_audio": feedback_audio_path})

@app.get("/")
def root():
    return {"message": "AI Interview System is running!"}