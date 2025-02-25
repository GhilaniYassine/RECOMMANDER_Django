from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import fitz, json, re
import google.generativeai as genai
from django.conf import settings

def upload_pdf(request):
    if request.method == 'POST' and request.FILES['pdf']:
        fs = FileSystemStorage()
        uploaded_file = request.FILES['pdf']
        filename = fs.save(uploaded_file.name, uploaded_file)
        text = extract_text(fs.path(filename))
        quiz_data = generate_quiz(text)
        
        # Store in session
        request.session['quiz_data'] = quiz_data
        return redirect('take_quiz')
        
    return render(request, 'quiz/upload.html')

def take_quiz(request):
    quiz_data = request.session.get('quiz_data')
    
    # Add debug print
    print("Quiz Data:", quiz_data)
    
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
    
    return render(request, 'quiz/quiz.html', {
        'quiz': quiz_data,
        'debug': settings.DEBUG  # Add this to show debug output in template
    })

def results(request):
    context = {
        'results': request.session.get('results'),
        'quiz_data': request.session.get('quiz_data')
    }
    return render(request, 'quiz/results.html', context)

# Helper functions (similar to Streamlit logic)
def extract_text(filepath):
    doc = fitz.open(filepath)
    return "".join([page.get_text() for page in doc])

def generate_quiz(text):
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-001')
    prompt = f"""Create a quiz question from this text with exactly:
    - 1 question
    - 3 possible answers (options)
    - Indicate the correct answer
    Format:
    Question: [question text]
    Options:
    1. [option1]
    2. [option2]
    3. [option3]
    Correct: [number of correct option]
    
    Text: {text}"""
    
    response = model.generate_content(prompt)
    
    # Add debug print
    print("AI Response:", response.text)
    
    try:
        lines = response.text.split('\n')
        quiz_data = {
            'questions': [{
                'question': '',
                'options': [],
                'correct_answer': None
            }]
        }
        
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
        
        # Add debug print
        print("Generated Quiz Data:", quiz_data)
        
        return quiz_data
    except Exception as e:
        print("Error generating quiz:", str(e))
        return {'questions': [], 'error': str(e)}