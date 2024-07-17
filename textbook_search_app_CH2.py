from flask import Flask, render_template, request, redirect, url_for, render_template_string, session
from werkzeug.utils import secure_filename
import requests
import webbrowser
from jinja2 import Environment, FileSystemLoader
from get_ebooks_function import get_books  
import os
import json
from pdfminer.high_level import extract_text # pip install pdfminer.six
from api_key import openai_api_key # format must be: openai_api_key = "123456789"
from openai import OpenAI


app = Flask(__name__)

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
    search_term = request.form.get('search_term')  
    search_type = request.form.get('search_type') # title, author, derived
    authors = request.form.get('authors')
    subject = request.form.get('subject')
    isbn = request.form.get('isbn')

    if search_type == "derived":
        if isbn != "None":
            query = f'isbn:{isbn}'
            books = get_books(query)
        else:
            query = f'"intitle:{search_term}" AND "inauthor:{authors}"'
            books = get_books(query)
            if len(books) == 0:
                query = f'"intitle:{search_term}"'
                books = get_books(query)
    else:
        query = f'{search_type}:"{search_term}" insubject:"{subject}"'
        books = get_books(query)
            
    return render_template('results.html', books=books)

@app.route('/open_ebook/<isbn>/<subject>/<author>', methods=['GET'])
def open_ebook(isbn, subject, author):
    env = Environment(loader=FileSystemLoader('ebooks'))
    template = env.get_template('google_ebook_reader_template.html')
    context = {'isbn': isbn}
    rendered_template = template.render(context)
    temp_html_file = os.path.abspath(f'ebooks/{subject}_by_{author}_ebook.html')
    with open(temp_html_file, 'w') as file:
        file.write(rendered_template)
    webbrowser.open('file://' + temp_html_file)
    
    # return to the previous page
    return render_template_string('''         
        <html><body><script>window.history.go(-1);</script></body></html>''')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_textbooks_info(syllabus_text):
    '''Extract textbook information from the syllabus text using OpenAI's GPT-3 model.
    Returns a list of dictionaries with textbook information.'''

    client  = app.config["client"]

    query_text = '''Extract information about any textbooks mentioned in the syllabus. Extract title, authors. If you can also extract publisher, edition, ISBN number, if textbooks are required or not. Also try to derive what scientific discipline or subject that textbook belongs to. Create a list of dictionaries in JSON format, one for each textbook,  in this format (showing example(!) values): [{"title": "Physics of the Atmosphere and Climate", "authors": "Salby, M., B. Thamdrup", "publisher": "Cambridge University Press", "edition": "2012", "isbn": "978-0-12-415955-6", "required": true, "subject": "atmospheric science}, etc. ]. "required" must be either true or false. For missing dictionary values use the Json value null. If no textbooks are mentioned return "Error: not textbooks found". The syllabus text is as follows:\n ''' + syllabus_text

    counter = 5
    while counter > 0:
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": query_text,
                        "max_tokens": 1500,
                        "temperature": 0.0,  # super deterministic only
                    }
                ],
                model="gpt-3.5-turbo",
            )   

            # choices is a list b/c we could request multiple answers but by default we only got 1 (which is fine)
            json_text = chat_completion.choices[0].message.content
        except Exception as e:
            print(f"Error with ChatGPT: {e}")
            time.sleep(5)
            counter -= 1
            continue

    if counter == 0:
        return None
    
    # When Ai return "Error: no textbooks found"
    if "error" in json_text.lower():
        return None

    # convert the JSON text to a list of dictionaries
    try:
        textbooks_list = json.loads(json_text)
    except json.JSONDecodeError:
        return None

    
    # Empty list to hold textbooks with all keys
    good_textbooks_list = []

    # Check that we got all keys and if not fill with ""
    keys = ["title", "authors", "publisher", "edition", "isbn", "required", "subject"]
    for textbook in textbooks_list:
        for key in keys:
            if key not in textbook: # fill in missing keys with empty strings
                textbook[key] = ""

    # check if any values are "null" and replace with None
    for textbook in textbooks_list:
        try:
            for key, value in textbook.items():
                if value == "null" or value == "Null":
                        textbook[key] = None
        except:
            pass # if there is an error just skip it
        finally:
            good_textbooks_list.append(textbook)

    return good_textbooks_list

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
            # Given that we know that the pdf location is valid 
            # This can't fail and will always return a string 
            text = process_syllabus(file_path)

            # Debugging: print the extracted textbooks
            #print("Extracted syllabus text:", text)


            # Debug: extract textbooks info from syllabus text using ChatGPT
            textbooks_info = extract_textbooks_info(text)

            if textbooks_info is None:
                textbooks_info = [{"title": "No textbooks found or error extracting textbook info."}]

            return render_template('syllabus_results.html', textbooks=textbooks_info)
    return render_template('upload_syllabus.html')

def process_syllabus(pdf):
 
    print(f"Processing syllabus file: {pdf}")
    text = extract_text(pdf)

    # remove newlines, extra spaces, etc.
    text = " ".join(text.split())

    return text

if __name__ == '__main__':
    app.run(debug=False, port=5000)

