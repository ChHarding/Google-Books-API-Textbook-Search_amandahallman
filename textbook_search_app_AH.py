from flask import Flask, render_template, request, redirect, url_for, render_template_string, session
from werkzeug.utils import secure_filename
import requests
import webbrowser
from jinja2 import Environment, FileSystemLoader
from get_ebooks_function import get_books  
import os
import fitz  # pip install PyMuPDF
from API_keys import openai_api_key # format must be: openai_api_key = "123456789"
from openai import OpenAI


app = Flask(__name__)

session["client"] = OpenAI(
    api_key
)


#UPLOAD_FOLDER = '.'
UPLOAD_FOLDER = 'uploads/'  # needs to end in a slash!!!
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DEBUG'] = True
app.config["client"] = OpenAI(
        api_key=openai_api_key # from API_keys.py
            )

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
            return redirect(request.url)
        file = request.files['syllabus_pdf']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Process uploaded syllabus PDF to extract textbooks
            textbooks = process_syllabus(file_path)

            # Debugging: print the extracted textbooks
            print("Extracted Textbooks:", textbooks)

            if not textbooks:
                textbooks.append("No textbook information found.")

            return render_template('syllabus_results.html', textbooks=textbooks)
    return render_template('upload_syllabus.html')

def process_syllabus(file_path):
    textbooks = []
    print(f"Processing syllabus file: {file_path}")
    with fitz.open(file_path) as doc:
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text()
            print(f"Page {page_num} Content:")
            print(text[:500])  # Print the first 500 characters of each page for debugging
            lines = text.split('\n')
            for line in lines:
                if "textbook" in line.lower() or "reading" in line.lower() :
                    textbooks.append(line.strip())
                    print(f"Found textbook line: {line.strip()}")

    if not textbooks:
        print("No textbook information found in the syllabus.")

    return textbooks

if __name__ == '__main__':
    app.run(debug=False, port=5000)

