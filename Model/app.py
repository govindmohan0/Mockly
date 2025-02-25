from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import fitz  # PyMuPDF
# import re

load_dotenv()

def read_pdf_and_extract_links(file_path):
    """Reads a PDF file, extracts text content, and identifies hidden links within the text.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        tuple: A tuple containing the text content of the PDF and a list of extracted links.
    """
    try:
        doc = fitz.open(file_path)
        text = ""
        # extracted_links = []
        github_links = []
        for page in doc:
            text += page.get_text()

            # Extract links using PyMuPDF (hidden links)
            # links = page.get_links()
        #     print(f"Debug: Number of links found on page: {len(links)}")  # Debug: Check number of links per page
        #     for link in links:
        #         # print(f"Debug: Link object: {link}") # Debug: Print link object to see what it is
        #         extracted_links.append(link['uri'])
        #         print(f"Debug: Extracted hidden link: {link['uri']}")  # Debug: Confirm link extraction

        #     # Extract links using regular expressions (visible links)
        #     url_pattern = re.compile(r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)')
        #     for match in url_pattern.finditer(text):
        #          extracted_links.append(match.group(0))
        #          print(f"Debug: Extracted visible link: {match.group(0)}")

        # # Remove duplicates
        # extracted_links = list(set(extracted_links))
            for link in page.get_links():
                url = link.get("uri", "")
                if "github.com" in url:
                    github_links.append({"platform": "GitHub", "url": url})

        return text, github_links

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None, []
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, []
        
file_path = "CVResume.pdf"
resume_text, resume_links = read_pdf_and_extract_links(file_path)
# print(resume_text)

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=False,
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Define AI Agents
resume_analyzer = Agent(
    role="Resume Analyzer",
    goal="Summarize key skills, experience, and education from the resume",
    backstory="You're an expert in parsing and analyzing resumes to extract structured insights.",
    llm=llm
)

question_generator = Agent(
    role="Interview Question Generator",
    goal="Generate tailored interview questions based on the resume",
    backstory="You specialize in crafting personalized interview questions for candidates based on their resumes.",
    llm=llm
)

interviewer = Agent(
    role="AI Interviewer",
    goal="Conduct structured interviews based on the resume data",
    backstory="You're an expert AI interviewer analyzing resumes and conducting interactive interviews.",
    llm=llm
)

response_analyzer = Agent(
    role="Response Analyzer",
    goal="Analyze responses and provide constructive feedback",
    backstory="You evaluate candidate responses, highlighting strengths and weaknesses for better assessment.",
    llm=llm
)

# Define Tasks
# extract_resume_data = Task(
#     description="Summarize key skills, experience, and education from the resume {data}.",
#     expected_output="Structured resume summary.",
#     agent=resume_analyzer,
# )

prepare_questions = Task(
    description=(
        "Generate a single, direct interview question based on the resume {data} and the candidate's previous answers. "
        "Do NOT include explanations, meta-comments, or placeholders like '(Waiting for response)'. "
        "Only return the next question."
    ),
    expected_output="A single interview question.",
    agent=question_generator,
)


conduct_interview = Task(
    description="Ask one direct interview question at a time based on {data}. Do not add unnecessary context or placeholders.",
    expected_output="A single interview question.",
    agent=interviewer,
)


analyze_responses = Task(
    description="Analyze the candidate's response {data} and provide a concise analysis (no more than 3 key strengths and 3 key areas for improvement). Avoid unnecessary rewording or excessive details.",
    expected_output="Concise interview feedback.",
    agent=response_analyzer,
)

# Create Crews
# resume_crew = Crew(
#     agents=[resume_analyzer],
#     tasks=[extract_resume_data],
#     process=Process.sequential,
# )

question_crew = Crew(
    agents=[question_generator],
    tasks=[prepare_questions],
    process=Process.sequential,
)

interview_crew = Crew(
    agents=[interviewer],
    tasks=[conduct_interview],
    process=Process.sequential,
)

response_crew = Crew(
    agents=[response_analyzer],
    tasks=[analyze_responses],
    process=Process.sequential,
)
# Run the process
# result = crew.kickoff(inputs={"resume": resume_text})
# print("CrewAI Process Result:", result)

# Interactive Interview Function
def interactive_interview(resume_data):
    """Conducts an interactive interview using CrewAI with structured questioning and feedback."""
    print("AI Interviewer: Let's begin the interview!")
    interview_transcript = []
    
    conversation_history = ""  # Maintain history of questions & responses

    while True:
        # Generate the next interview question dynamically
        questions = question_crew.kickoff(
                        inputs={
                            "data": f"Resume details: {resume_data}. Previous responses: {conversation_history}. "
                                    "Provide the next question only, without any additional descriptions or meta-comments."
                        }
                    )

        question = interview_crew.kickoff(inputs={"data": questions})
        
        print(f"AI Interviewer: {question}")

        # Get user response
        user_response = input("Your answer: ")

        if user_response.lower() in ["exit", "quit", "stop"]:
            print("AI Interviewer: Thank you for your time! The interview is now complete.")
            break

        # Evaluate the response
        feedback = response_crew.kickoff(inputs={"data": f"Candidate's response: {user_response}. Provide feedback."})
        print(f"AI Interviewer Feedback: {feedback}")

        # Store conversation history (to be used in next question generation)
        conversation_history += f"\nQ: {question}\nA: {user_response}\nFeedback: {feedback}\n"

        # Store transcript
        interview_transcript.append({"question": question, "answer": user_response, "feedback": feedback})

    return interview_transcript


# Start AI-driven interview
interview_transcript = interactive_interview(resume_text)
print("Final Interview Transcript:", interview_transcript)
# The course which I have been continuously working on is data dtructure and algorithm. I faced many challenges in building logics to solve the DSA prob
# lems but with time and dedication and help from some youtube videos I have been good at solving easy and medium level coding problems. I have good knowledge and in
# terest in machine learning as well. I have recently developed a deep learning model for crop disease detection which takes image of plant leaves as image to claasi
# fy the image and generate prevention measures and cure for better crop yield.