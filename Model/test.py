import dotenv
from crewai import Agent, Task, Crew
import chainlit as cl
from langchain_google_genai import ChatGoogleGenerativeAI
# import os
import os

os.environ["CHAINLIT_LANG"] = "en-GB"

dotenv.load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

interviewer = Agent(
    role='Interviewer',
    goal='Ask thoughtful questions related to the candidates field, assess skills, and evaluate responses.',
    backstory='You are an expert interviewer assessing candidates for technical and behavioral competencies.',
    verbose=True,
    allow_delegation=False,
    llm=llm,
)

evaluator = Agent(
    role='Evaluator',
    goal='Evaluate the responses given by the candidate based on correctness, clarity, and relevance.',
    backstory='You are a hiring expert analyzing interview answers and providing feedback.',
    verbose=True,
    allow_delegation=False,
    llm=llm,
)

task1 = Task(
    description=f"""Ask the candidate a technical question based on their expertise and field.""",
    agent=interviewer,
    expected_output="A well-structured question relevant to the user's expertise.",
)

task2 = Task(
    description=f"""Analyze the candidate's response and provide constructive feedback, highlighting strengths and weaknesses.""",
    agent=evaluator,
    expected_output="Detailed analysis of the response with a score and improvement suggestions.",
)


@cl.on_chat_start
async def on_chat_start():
    global question
    question_task = Task(
        description=f"Ask the candidate a technical question based on their expertise and field.",
        agent=interviewer,
        expected_output="A well-structured question relevant to the user’s expertise.",
    )

    crew = Crew(agents=[interviewer], tasks=[question_task], verbose=1)
    question = crew.kickoff()[0]  # Get the generated question
    
    await cl.Message(content=f"Question: {question}").send()
    await cl.Message(content="Please provide your response.").send()

@cl.on_message
async def on_message(message):
    user_response = message.content

    evaluation_task = Task(
        description=f"Analyze the response: {user_response} and provide constructive feedback.",
        agent=evaluator,
        expected_output="Detailed feedback with strengths, weaknesses, and a score.",
    )

    crew = Crew(agents=[evaluator], tasks=[evaluation_task], verbose=1)
    feedback = crew.kickoff()[0]  # Get the feedback response

    await cl.Message(content=f"Feedback: {feedback}").send()