import requests
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, UserProfile
from django.http import HttpResponseForbidden
import chardet
import spacy
from .models import UserProfile

nlp = spacy.load("en_core_web_sm")


@login_required
def profile(request):
    if request.method == "POST":
        uname = request.POST['username']
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        email = request.POST['email']
        curr_class = request.POST['curr_class']
        ed_bg = request.POST['board']
        school = request.POST['school']
        hobbies = request.POST['hobbies']
        skills = request.POST['skills']
        certifications = request.POST['certifications']
    else:
        user = request.user
        uname = user.username
        fname = user.first_name
        lname = user.last_name
        email = user.email
        try:
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            curr_class = user_profile.curr_class
            ed_bg = user_profile.board
            school = user_profile.school
            hobbies = user_profile.hobbies
            skills = user_profile.skills
            certifications = user_profile.certifications
        except UserProfile.DoesNotExist:
            curr_class = ''
            ed_bg = ''
            school = ''
            hobbies = ''
            skills = ''
            certifications = ''

    context = {
        'username': uname,
        'first_name': fname,
        'last_name': lname,
        'email': email,
        'curr_class': curr_class,
        'board': ed_bg,
        'school': school,
        'hobbies': hobbies,
        'skills': skills,
        'certifications': certifications,
    }
    return render(request, 'profile.html', context)


def login_user(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        # user = User.objects.get(email=email)

        user, is_user_created = User.objects.get_or_create(
            email=email, username=email.split('@')[0]
        )

        if not is_user_created:
            # User already exists
            if getattr(user, 'has_usable_password', None) and user.has_usable_password():
                # Existing user trying to sign 
                print("User has a usable password")
            else:
                print("User does not have a usable password")
        else:
            print("USER IS CREATED")

        if user:
            try:
                user = authenticate(username=email.split('@')[0], password=password)
            except Exception as e:
                return HttpResponseForbidden("Something went wrong")
            print(user)
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "User Does not exist")
            return redirect('login_user')

    else:
        return render(request, 'login.html')


@login_required
def logout_user(request):
    logout(request)
    return redirect('login_user')


@login_required
def register(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        username = email.split('@')[0]

        if password == cpassword:
            if not User.objects.get(email=email):
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                print(fname, lname, email, password)
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "User already exist please login")
                return redirect('login_user')
        else:
            messages.error(request, "Password does not match")
    else:
        return render(request, 'register.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def prereq_analysis(request):
    if request.method == "POST":
        course = "frontend"
        board = "CBSE"

        response = requests.post("http://127.0.0.1:8000/prereq_analysis/", json={
            'course': course,
            'board': board
        })
        print(response)

        if response.status_code == 200:
            print(response.json())
        else:
            print("\nfailed\n")
        return render(request, template_name="prereq.html")

    return render(request, template_name="prereq.html")


@login_required
def comparative_analysis(request):
    if request.method == "POST":
        # job_description_file = request.FILES['job_description']
        # resume_file = request.FILES['resume']
        # with fitz.open(stream=job_description_file.read(), filetype="pdf") as job_desc_pdf:
        #     job_description = " ".join(page.get_text() for page in job_desc_pdf)
        #
        # with fitz.open(stream=resume_file.read(), filetype="pdf") as resume_pdf:
        #     resume = " ".join(page.get_text() for page in resume_pdf)

        job_description = """
        
        We are seeking a talented Web Developer to join our team. You will be responsible for developing and maintaining high-quality web applications using cutting-edge technologies. The ideal candidate will have a strong background in front-end and back-end development, with expertise in React, Vue.js, Webpack, and a Backend Framework such as Django or Flask.

        Responsibilities:
        
            Develop new user-facing features using React, Vue.js, and other modern web technologies
            Build reusable components and front-end libraries for future use
            Optimize applications for maximum speed and scalability
            Implement and maintain web APIs using Django, Flask, or similar frameworks
            Collaborate with other team members and stakeholders to deliver high-quality software solutions
            Stay up-to-date with emerging technologies and trends in web development
        
        Requirements:
        
            Bachelor's degree in Computer Science or a related field
            Proven work experience as a Web Developer, with a strong portfolio of web applications
            Proficiency in React, Vue.js, Webpack, and a Backend Framework (e.g., Django, Flask)
            Experience with version control systems such as Git
            Solid understanding of web technologies, including HTML, CSS, JavaScript, and AJAX
            Strong problem-solving skills and attention to detail
            Excellent communication and teamwork abilities
        
        
        """

        resume = """
        
        Highly skilled Web Developer with 5+ years of experience designing and developing responsive websites and web applications. Proficient in HTML, CSS, JavaScript, and version control using Git. Strong background in implementing responsive design principles to ensure optimal user experience across devices.

        Experience:
        
        Web Developer
        [Company Name] - [Location]
        [Dates of Employment]
        
            Developed and maintained websites for clients, ensuring high performance, responsiveness, and user-friendly design
            Collaborated with designers and backend developers to implement front-end functionality using HTML, CSS, and JavaScript
            Implemented version control using Git to track changes and manage codebase efficiently
        
        Frontend Developer
        [Company Name] - [Location]
        [Dates of Employment]
        
            Created interactive user interfaces using HTML, CSS, and JavaScript
            Optimized websites for speed and performance, following best practices for responsive design
            Conducted code reviews and provided feedback to team members to improve code quality
        
        Skills:
        
            Proficient in HTML, CSS, JavaScript
            Experience with responsive design principles
            Familiarity with version control systems (e.g., Git)
            Strong problem-solving and analytical skills
            Excellent communication and teamwork abilities
        
        Education:
        Bachelor's Degree in Computer Science
        [University Name] - [Location]
        [Dates of Attendance]
        
        Certifications:
        
            Responsive Web Design Certification
            Git Fundamentals Certification
        
        Projects:
        
            [Project Name]: Developed a responsive website for a local business, increasing online visibility and customer engagement
        
        Languages:
        
            English (Fluent)
        
        
        """

        job_desc_doc = nlp(job_description)
        resume_doc = nlp(resume)

        job_desc_tokens = [token.lemma_.lower() for token in job_desc_doc if
                           not token.is_stop and not token.is_punct]
        resume_tokens = [token.lemma_.lower() for token in resume_doc if not token.is_stop and not token.is_punct]

        job_desc_set = set(job_desc_tokens)
        resume_set = set(resume_tokens)

        keyword_coverage = len(resume_set.intersection(job_desc_set)) / len(job_desc_set) if len(
            job_desc_set) > 0 else 0
        resume_score = keyword_coverage * 100
        print(f"Resume Score: {resume_score}")
        context = {
            "score": resume_score
        }
        return render(request, 'comparative.html', context)
    return render(request, 'comparative.html')
