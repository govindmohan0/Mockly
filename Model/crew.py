from crewai import Crew, Task, Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()
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