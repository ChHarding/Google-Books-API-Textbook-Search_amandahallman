from flask import Flask, render_template, request, redirect, url_for, render_template_string, session
from werkzeug.utils import secure_filename
import requests
import webbrowser
from jinja2 import Environment, FileSystemLoader
from get_ebooks_function import get_books  
import os
import fitz  # pip install PyMuPDF
from api_key import openai_api_key # format must be: openai_api_key = "123456789"
from openai import OpenAI
from pdfminer.high_level import extract_text
import json
from pprint import pprint


app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)  # From api_key.py

#api_key = openai_api_key

#app.secret_key = 'your_secret_key'


#session["client"] = OpenAI(
    #api_key
#)


#UPLOAD_FOLDER = '.'
UPLOAD_FOLDER = 'syllabus_pdf/'  # needs to end in a slash!!!
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DEBUG'] = True
app.config["client"] = client


@app.route('/', methods=['GET'])
def index():
    return render_template('search_w_autocomplete.html')

@app.route('/search', methods=['POST'])
def perform_search():
    search_term = request.form['search_term']
    search_type = request.form['search_type']
    subject = request.form['subject']

    query = f'{search_type}:"{search_term}" insubject:"{subject}"'
    books = get_books(query)
    
    return render_template('results.html', books=books)

@app.route('/open_ebook/<isbn>/<subject>/<author>', methods=['GET'])
def open_ebook(isbn, subject, author):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('google_ebook_reader_template.html')
    context = {'isbn': isbn}
    rendered_template = template.render(context)
    temp_html_file = os.path.abspath(f'{subject}_by_{author}_ebook.html')
    with open(temp_html_file, 'w') as file:
        file.write(rendered_template)
    webbrowser.open('file://' + temp_html_file)
    
    return render_template_string('''         
        <html><body><script>window.history.go(-1);</script></body></html>''')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_syllabus', methods=['GET', 'POST'])
def upload_syllabus():
    if request.method == 'POST':
        if 'syllabus_pdf' not in request.files:
            print("No file part in the request")
            return redirect(request.url)
        
        file = request.files['syllabus_pdf']
        if file.filename == '':
            print("No selected file")
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Process uploaded syllabus PDF to extract textbooks
            textbooks = extract_textbook_from_syllabus(client, file_path)
            #process_syllabus(file_path)

            # Debugging: print the extracted textbooks
            print("Extracted Textbooks:", textbooks)

            if not textbooks:
                textbooks.append("No textbook information found.")

            return render_template('syllabus_results.html', textbooks=textbooks)
    return render_template('upload_syllabus.html')

# TAKEN FROM process_ChatGPT_CH (below)

def extract_textbook_from_syllabus(client, pdf):
    # Convert PDF to text
    syllabus_text = extract_text(pdf)

    # Remove newlines, extra spaces, etc.
    syllabus_text = " ".join(syllabus_text.split())

    # Call the function to extract textbooks using OpenAI API
    text_book_list = extract_textbooks(client, syllabus_text)
    return text_book_list


def extract_textbooks(client, syllabus_text):
    query_text = '''Extract information about any textbooks mentioned in the syllabus. Extract title, authors, publisher, edition, ISBN number, if they are required or not, and create a list of dictionaries in JSON format in this format (showing example values): [{"title": "Physics of the Atmosphere and Climate", "authors": "Salby, M., B. Thamdrup", "publisher": "Cambridge University Press", "edition": "2012", "isbn": "978-0-12-415955-6", "required": true}, etc. ]. "required" must be either true or false. For missing dictionary values use the JSON null. If no textbooks are mentioned return "Error: no textbooks found". The syllabus text is as follows: ''' + syllabus_text

    try:
        completion = client.Completion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": query_text,
                    "max_tokens": 1500,
                    "temperature": 0.0,  # super deterministic only
                }
            ],
        )
    except openai.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return None

    # Extract the JSON text from the response
    json_text = completion['choices'][0]['message']['content']

    # Convert the JSON text to a list of dictionaries
    try:
        textbooks_list = json.loads(json_text)
    except json.JSONDecodeError:
        return None
    
    # Catch the error case
    if "Error" in textbooks_list[0] or "error" in textbooks_list[0]:
            return None

    return textbooks_list


'''
def process_syllabus(file_path):
    textbooks = []
    print(f"Processing syllabus file: {file_path}")
    
    with fitz.open(file_path) as doc:
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text()
            lines = text.split('\n')
            for line in lines:
                # Lowercase the line for easier keyword matching
                lower_line = line.lower()
                if "textbook" in lower_line or "required reading" in lower_line or "recommended reading" in lower_line:
                    textbooks.append(line.strip())
                    print(f"Found textbook line: {line.strip()}")
                # Optional: Add more sophisticated parsing here
                # For example, using regular expressions to match ISBN or title-author patterns

    if not textbooks:
        print("No textbook information found in the syllabus.")

    return textbooks
'''
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)

