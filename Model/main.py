from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

load_dotenv()

app = FastAPI()

# Initialize AI Model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Define Interview Agent
interviewer = Agent(
    role="AI Interviewer",
    goal="Conduct structured interviews based on resume data",
    backstory="You're an expert AI interviewer analyzing resumes.",
    llm=llm,
    allow_delegation=True,
    verbose=True
)

# Define API Request Model
class InterviewRequest(BaseModel):
    resume_text: str

@app.post("/start-interview")
async def start_interview(request: InterviewRequest):
    try:
        resume_text = request.resume_text
        initial_question = llm.invoke(f"Based on the resume, ask an appropriate interview question: {resume_text}")
        
        return {"question": initial_question.content if hasattr(initial_question, 'content') else str(initial_question)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Accept User Response & Generate Next Question
class ResponseRequest(BaseModel):
    question: str
    user_answer: str

@app.post("/next-question")
async def next_question(request: ResponseRequest):
    try:
        feedback = llm.invoke(f"Evaluate this response: Q: {request.question} | A: {request.user_answer}. Provide feedback and suggest the next best question.")
        return {"next_question": feedback.content if hasattr(feedback, 'content') else str(feedback)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run Backend
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
