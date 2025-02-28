from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from crewai import Crew
from dotenv import load_dotenv
from tempfile import NamedTemporaryFile
import os
import fitz 

load_dotenv()

from crewai import Task, Agent
from langchain_google_genai import ChatGoogleGenerativeAI

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "http://localhost:5173",  # Your React frontend
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Initialize Gemini AI Model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=False,
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

question_generator = Agent(
    role="Interview Question Generator",
    goal="Generate tailored interview questions based on the resume",
    backstory="You specialize in crafting personalized interview questions for candidates based on their resumes.",
    llm=llm
)

response_analyzer = Agent(
    role="Response Analyzer",
    goal="Analyze responses and provide constructive feedback",
    backstory="You evaluate candidate responses, highlighting strengths and weaknesses for better assessment.",
    llm=llm
)

# Define Tasks
prepare_questions = Task(
    description="Generate a single interview question based on the {data}.",
    expected_output="A single interview question.",
    agent=question_generator,
)

analyze_responses = Task(
    description="Analyze the candidate's response {data} and provide a concise analysis.",
    expected_output="Concise interview feedback.",
    agent=response_analyzer,
)

# Create Crews
question_crew = Crew(
    agents=[question_generator],
    tasks=[prepare_questions],
)

response_crew = Crew(
    agents=[response_analyzer],
    tasks=[analyze_responses],
)

class ResumeInput(BaseModel):
    data: str  # Ensure the frontend sends `data` as a JSON field

def extract_resume_text_and_links(pdf_file):
    """Extract text and GitHub links from a resume PDF."""
    try:
        doc = fitz.open(pdf_file)
        text = ""
        github_links = []

        for page in doc:
            text += page.get_text()
            for link in page.get_links():
                url = link.get("uri", "")
                if "github.com" in url:
                    github_links.append({"platform": "GitHub", "url": url})

        return text, github_links

    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None, []


@app.post("/upload_resume/")
async def upload_resume(file: UploadFile = File(...)):
    """Handles resume upload and extracts key data."""
    with NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    resume_text, resume_links = extract_resume_text_and_links(temp_file_path)
    os.remove(temp_file_path)

    if resume_text:
        return {"message": "Resume processed", "parsed_data": resume_text, "links": resume_links}
    else:
        return {"message": "Failed to extract resume content"}


@app.post("/generate_questions/")
async def generate_questions(resume_data: ResumeInput):
    """Generates interview questions based on the resume."""
    result = question_crew.kickoff(inputs={"data": resume_data})
    return {"questions": result}


class ResponseModel(BaseModel):
    question: str
    response: str


@app.post("/evaluate_response/")
async def evaluate_response(response_model: ResponseModel):
    """Evaluates interview responses and provides AI feedback."""
    try:
        evaluation = response_crew.kickoff(inputs={"data": response_model.response})
        next_question = question_crew.kickoff(inputs={"data": f"Resume details: {response_model.response}. Previous responses: {response_model.question}. "
                                        "Provide the next question only, without any additional descriptions or meta-comments."})
        return {"evaluation": evaluation, "next_question": next_question}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing response: {str(e)}")


@app.get("/")
def root():
    return {"message": "AI Interview System is running!"}

# run using:- uvicorn main:app --reload
# or fastapi dev main.py