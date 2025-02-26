# Django PDF Quiz Generator - Code Explanation

## Overview
This Django application processes PDF files, extracts text, generates a quiz question using Google's Generative AI (Gemini API), and allows users to take the quiz and view results.

## Code Breakdown

### 1. Importing Dependencies
```python
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import fitz, json, re
import google.generativeai as genai
from django.conf import settings
```
- `render, redirect`: Used to render templates and redirect users between views.
- `FileSystemStorage`: Handles file uploads (saving and retrieving uploaded PDFs).
- `fitz` (PyMuPDF): Extracts text from PDFs.
- `google.generativeai`: Connects to Google's Gemini AI for quiz generation.
- `settings`: Accesses Django settings (like API keys).

---

### 2. Uploading the PDF and Extracting Text
```python
def upload_pdf(request):
    if request.method == 'POST' and request.FILES['pdf']:  
        fs = FileSystemStorage()
        uploaded_file = request.FILES['pdf']
        filename = fs.save(uploaded_file.name, uploaded_file)  
        
        text = extract_text(fs.path(filename))  
        quiz_data = generate_quiz(text)  
        
        request.session['quiz_data'] = quiz_data  
        return redirect('take_quiz')  

    return render(request, 'quiz/upload.html')  
```
### What happens here?
1. Checks if a PDF file is uploaded.
2. Saves the file.
3. Extracts text and generates a quiz.
4. Stores the quiz in session and redirects the user.

---

### 3. Taking the Quiz
```python
def take_quiz(request):
    quiz_data = request.session.get('quiz_data')  
    
    if request.method == 'POST':  
        score = 0
        user_answer = request.POST.get('answer')  
        
        if user_answer is not None:
            user_answer = int(user_answer.replace('option', '')) - 1  
            if user_answer == quiz_data['questions'][0]['correct_answer']:  
                score = 1  
        
        request.session['results'] = {  
            'score': score,
            'total': 1,
            'user_answer': user_answer,
            'correct_answer': quiz_data['questions'][0]['correct_answer']
        }
        return redirect('results')  

    return render(request, 'quiz/quiz.html', {'quiz': quiz_data})
```
### What happens here?
1. Retrieves quiz data.
2. Checks user answer and evaluates score.
3. Stores results and redirects to results page.

---

### 4. Displaying the Results
```python
def results(request):
    context = {
        'results': request.session.get('results'),
        'quiz_data': request.session.get('quiz_data')
    }
    return render(request, 'quiz/results.html', context)
```
### What happens here?
1. Retrieves quiz results from session.
2. Displays them on the results page.

---

### 5. Extracting Text from PDF
```python
def extract_text(filepath):
    doc = fitz.open(filepath)  
    return "".join([page.get_text() for page in doc])  
```
- Uses `fitz` (PyMuPDF) to extract text from the PDF.

---

### 6. Generating Quiz using AI
```python
def generate_quiz(text):
    genai.configure(api_key=settings.GEMINI_API_KEY)  
    model = genai.GenerativeModel('gemini-1.5-flash-001')  

    prompt = (
        "Create a quiz question from this text with exactly:
"
        "- 1 question
"
        "- 3 possible answers (options)
"
        "- Indicate the correct answer
"
        "Format:
"
        "Question: [question text]
"
        "Options:
"
        "1. [option1]
"
        "2. [option2]
"
        "3. [option3]
"
        "Correct: [number of correct option]

"
        f"Text: {text}"
    )

    response = model.generate_content(prompt)  

    try:
        lines = response.text.split('\n')  
        quiz_data = {'questions': [{'question': '', 'options': [], 'correct_answer': None}]}
        
        for line in lines:
            line = line.strip()
            if line.startswith('Question:'):
                quiz_data['questions'][0]['question'] = line.replace('Question:', '').strip()
            elif line.startswith('1.'):
                quiz_data['questions'][0]['options'].append(line[2:].strip())
            elif line.startswith('2.'):
                quiz_data['questions'][0]['options'].append(line[2:].strip())
            elif line.startswith('3.'):
                quiz_data['questions'][0]['options'].append(line[2:].strip())
            elif line.startswith('Correct:'):
                quiz_data['questions'][0]['correct_answer'] = int(line.replace('Correct:', '').strip()) - 1
        
        return quiz_data
    except Exception as e:
        return {'questions': [], 'error': str(e)}
```
### What happens here?
1. Configures Gemini AI and prompts it to generate a quiz.
2. Parses AI response into structured quiz data.

---

## Summary
This Django app:
1. Uploads a PDF and extracts text.
2. Uses Google Gemini AI to generate quiz questions.
3. Displays the quiz and evaluates user responses.
4. Stores results in session and displays them.

Let me know if you need modifications! 🚀
