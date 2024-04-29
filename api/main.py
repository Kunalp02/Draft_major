from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import openai
import json
import spacy
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
JSON_FILE_PATH = "./dataset.json"
MODEL_NAME = "en_core_web_sm"

COURSE_PREREQUISITES = {
    "web_developer": ["Html", "Css", "JavaScript", "Responsive Design", "Version Control (e.g., Git)"],
    "react_developer": ["Html", "Css", "JavaScript", "React", "Version Control (e.g., Git)"],
    "python_developer": ["Python", "Django", "Flask", "SQL", "Version Control (e.g., Git)"],
    "angular_developer": ["Html", "Css", "JavaScript", "Angular", "TypeScript", "Version Control (e.g., Git)"],
    "ui_ux_designer": ["Design Principles", "Wireframe", "Prototyping", "Adobe XD", "Figma", "Sketch"],
    "devops_engineer": ["Linux", "Networking", "Scripting", "CI/CD", "Docker", "Kubernetes", "Version Control (e.g., Git)"],
    "full_stack_developer": ["Html", "Css", "JavaScript", "React", "Node.js", "Express", "MongoDB", "Version Control (e.g., Git)"],
    "software_developer": ["Data Structures", "Algorithms", "Object-Oriented Programming", "Version Control (e.g., Git)"],
    "frontend_developer": ["Html", "Css", "JavaScript", "Responsive Design", "Version Control (e.g., Git)"],
    "mobile_app_developer": ["Programming Language (e.g., Swift, Java, Kotlin)", "Mobile Development Framework (e.g., React Native, Flutter)", "Version Control (e.g., Git)"],
    "data_scientist": ["Programming Language (e.g., Python, R)", "Statistics", "Data Manipulation and Cleaning", "Machine Learning", "Version Control (e.g., Git)"],
    "cloud_engineer": ["Linux", "Networking", "Scripting (e.g., Bash, Python)", "Version Control (e.g., Git)"],
    "quality_assurance_engineer": ["Understanding of SDLC", "Testing Concepts", "Test Case Design", "Bug Tracking", "Version Control (e.g., Git)"],
    "cybersecurity_specialist": ["Networking", "Operating Systems", "Security Fundamentals", "Scripting (e.g., Python)", "Version Control (e.g., Git)"]
}

COURSE_RECOMMENDATIONS = {
    "web_developer": ["React", "Vue.js", "Webpack", "Backend Framework (e.g., Django, Flask)"],
    "react_developer": ["Advanced React", "State Management (e.g., Redux, Context API)", "React Router"],
    "python_developer": ["Advanced Python", "API Development", "Web Scraping", "Async Programming"],
    "angular_developer": ["Advanced Angular", "Angular CLI", "RxJS", "Unit Testing"],
    "ui_ux_designer": ["User Research", "Interaction Design", "Visual Design", "Responsive Design Principles"],
    "devops_engineer": ["Infrastructure as Code (e.g., Terraform)", "Cloud Services (e.g., AWS, Azure, GCP)", "Monitoring and Logging Tools"],
    "full_stack_developer": ["Authentication and Authorization", "GraphQL", "RESTful APIs", "CI/CD Pipelines"],
    "software_developer": ["Design Patterns", "Database Management", "Testing Frameworks"],
    "frontend_developer": ["CSS Preprocessors (e.g., Sass, Less)", "Frontend Frameworks (e.g., React, Angular, Vue.js)", "Build Tools (e.g., Webpack, Gulp)"],
    "mobile_app_developer": ["Mobile UI Frameworks (e.g., UIKit for iOS, Android Jetpack)", "API Integration", "Mobile Security"],
    "data_scientist": ["Data Visualization (e.g., Matplotlib, Seaborn)", "Big Data Technologies (e.g., Hadoop, Spark)", "Deep Learning"],
    "cloud_engineer": ["Cloud Platforms (e.g., AWS, Azure, GCP)", "Infrastructure as Code (e.g., Terraform)", "Containerization (e.g., Docker, Kubernetes)"],
    "quality_assurance_engineer": ["Test Automation Tools (e.g., Selenium, Appium)", "Performance Testing", "Security Testing"],
    "cybersecurity_specialist": ["Ethical Hacking", "Security Certifications (e.g., CISSP, CEH)", "Security Tools (e.g., Nmap, Wireshark)"]
}



class CourseInput(BaseModel):
    course: str
    board: str


class CourseOutput(BaseModel):
    # board: str
    # highest_class: str
    # prerequisite_skills: List[str]
    # completed_skills: List[str]
    # recommended_skills: List[str]
    # uncovered_skills: List[str]
    prompt: str


def find_remaining_skills(data, board, prerequisite_skills, completed_skills):
    highest_class = None
    remaining_skills = set(prerequisite_skills)

    if board in data:
        for class_name, subjects in data[board].items():
            for subject_name, topics in subjects.items():
                for topic in topics:
                    doc = nlp(topic)

                    for skill in set(remaining_skills):
                        if skill.lower() in [token.text.lower() for token in doc]:
                            completed_skills.add(skill)
                            remaining_skills.remove(skill)

            if not remaining_skills:
                highest_class = class_name
                break

    return highest_class, completed_skills


def load_dataset(file_path):
    try:
        with open(file_path, 'r') as file:
            dataset = json.load(file)
        return dataset
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Unable to decode JSON from {file_path}")
        return None


def load_spacy_model(model_name):
    try:
        return spacy.load(model_name)
    except OSError:
        print(
            f"Error: SpaCy model '{model_name}' not found. Make sure it's installed or download it using `python -m "
            f"spacy download en_core_web_sm`.")
        return None


def find_uncovered_skills(recommended_skills, completed_skills):
    return list(set(skill for skill in recommended_skills if skill not in completed_skills))


@app.post("/prereq_analysis", response_model=CourseOutput)
def get_course_results(course_input: CourseInput):
    course = course_input.course.lower()
    edboard = course_input.board.lower()

    if course in COURSE_PREREQUISITES:
        prerequisite_skills = COURSE_PREREQUISITES[course]
        recommended_skills = COURSE_RECOMMENDATIONS.get(course, [])

        board = edboard
        completed_skills = set()

        highest_class, completed_skills = find_remaining_skills(data, board, prerequisite_skills, completed_skills)

        if highest_class:
            uncovered_skills = find_uncovered_skills(recommended_skills, completed_skills)
            print("Uncovered skills")
            prompt = f"""
                Career Guidance: Job Role Analysis
                Job Role: {course}
                Prerequisite Analysis:
                
                    Highest Class Completed: {highest_class}
                    Board/University: {board}
                
                Prerequisite Skills:
                
                    Completed Skills: {completed_skills}
                    Recommended Skills: {recommended_skills}
                    Uncovered Skills: {uncovered_skills}
                
                Analysis Summary:
                
                Based on your current qualifications and skills, here's an overview of your readiness for the job role:
                
                    Prerequisites Met: You meet the prerequisites for this Course.
                    Skills to Learn:
                        [List of skills you need to learn]
                    Recommended Path:
                        Follow these steps to prepare for the role:
                            [Step 1: e.g., Gain experience in XYZ]
                            [Step 2: e.g., Complete a course in ABC]
                            [Step 3: e.g., Obtain certification in DEF]
                            
                Generate recommendation for user based on the given data and in above format.
                can you return the response text and format it as markdown
                can you look at the structure and use the appropriate #,## or ###
                , plus any bullet points , hyperlinks or codeblocks in your output.
            """

            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                temperature=0,
                max_tokens=2000,
                messages=[
                    {"role": "system", "content": f"{prompt}"}
                ]
            )

            response_text = f"{completion.choices[0].message['content']}"
            print("\n\n\n\n", response_text)

            return CourseOutput(
                prompt=response_text
            )
        else:
            return {"detail": f"No class found for {course} where all prerequisite skills are matched."}
    else:
        return {"detail": "Invalid course. Please check your input."}

if __name__ == "__main__":
    data = load_dataset(JSON_FILE_PATH)
    if data is None:
        exit()

    nlp = load_spacy_model(MODEL_NAME)
    if nlp is None:
        exit()

    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
    