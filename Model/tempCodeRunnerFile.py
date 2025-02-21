import os
import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv  # Load .env file

# Load environment variables from .env file
load_dotenv()

# Get API key from .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Check if API key is loaded correctly
if not GEMINI_API_KEY:
    raise ValueError("⚠️ API key not found! Make sure you have a .env file with GEMINI_API_KEY.")

### 1️⃣ Extract hyperlinks from PDF ###
def extract_hyperlinks(pdf_path):
    doc = fitz.open(pdf_path)
    links = []

    for page in doc:
        for link in page.get_links():
            url = link.get("uri", "")
            if "linkedin.com" in url:
                links.append({"platform": "LinkedIn", "url": url})
            elif "github.com" in url:
                links.append({"platform": "GitHub", "url": url})

    return links

### 2️⃣ Scrape GitHub profile data ###
def scrape_github_profile(github_url):
    headers = {"User-Agent": "Mozilla/5.0"}  # Avoid bot detection
    response = requests.get(github_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        name = soup.find("span", class_="p-name").text.strip() if soup.find("span", class_="p-name") else "No Name"
        bio = soup.find("div", class_="p-note").text.strip() if soup.find("div", class_="p-note") else "No Bio"

        return {"name": name, "bio": bio, "url": github_url}
    else:
        return None

### 3️⃣ Generate questions using Gemini 2.0 Flash ###
def generate_questions(profile_data):
    if not profile_data:
        return "No valid profile data to generate questions."

    prompt = f"""
    Based on the following GitHub profile, generate 5 technical interview questions:
    
    Name: {profile_data['name']}
    Bio: {profile_data['bio']}
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return response.text if response else "Failed to generate questions."

### 4️⃣ Main Workflow ###
pdf_path = r"C:/Users/hkanv/Desktop/Govind Mohan Shah Resume.pdf"
profile_links = extract_hyperlinks(pdf_path)

for link in profile_links:
    if link["platform"] == "GitHub":
        print(f"\nScraping GitHub profile: {link['url']} ...")
        github_data = scrape_github_profile(link["url"])
        
        if github_data:
            print(f"\nGenerating questions for {github_data['name']} ...")
            questions = generate_questions(github_data)
            print("\n🔹 AI-Generated Interview Questions:")
            print(questions)
