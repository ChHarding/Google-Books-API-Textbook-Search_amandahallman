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


app = Flask(__name__) # creates Flask application

#UPLOAD_FOLDER = '.'
UPLOAD_FOLDER = 'uploads/'  # needs to end in a slash, directory where uploaded files will be saved
ALLOWED_EXTENSIONS = {'pdf'} # set of file extensions that are allowed for uplaods (only PDFs for this)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER # set folder where uploads will be saved
app.config['DEBUG'] = True
app.config["client"] = OpenAI(
        api_key=openai_api_key # from API_keys.py, initialize the OpenAI client with the API key
            )

@app.route('/', methods=['GET'])
def index():
    '''Renders the main search page.
    
    This functions handles GET requests to the root URL ('/'). It returns
    the HTML template for the main search page with autocomplete functionality.

    Returns:
        str: Rendered HTML template for the search page.
    '''
    return render_template('search_w_autocomplete.html') # renders the main search page, returns HTML template (search_w_auto..)

@app.route('/search', methods=['POST'])
def perform_search():
    '''Performs a book search based on the given parameters.
    
    This function handles POST requests to the '/search' URL. It retrieves the
    search parameters from the form data, constructs a query based on the search
    type and parameters, and fetches book data using the 'get_books' function.
    The results are then rendered in the 'results.html' template.
    
    Returns:
        str: Rendered HTML template with the search results.
    
    Form Data:
        search_term (str): The search term entered by the user.
        search_type (str): The type of search (e.g., title, author, derived).
        authors (str): The authors specified by the user.
        subject (str): The subject specified by the user.
        isbn (str): The ISBN number specified by the user.
    '''
    search_term = request.form.get('search_term')  
    search_type = request.form.get('search_type')
    authors = request.form.get('authors')
    subject = request.form.get('subject')
    isbn = request.form.get('isbn')

    if search_type == "derived":
        if isbn != "None": # if isbn is provided, creates a query to search by ISBN
            query = f'isbn:{isbn}'
            books = get_books(query)
        else: # otherwise, construct query to search by title and author
            query = f'"intitle:{search_term}" AND "inauthor:{authors}"'
            books = get_books(query)
            if len(books) == 0:
                query = f'"intitle:{search_term}"'
                books = get_books(query)
    else: # otherwise, construct query based on 'search_type', subject
        query = f'{search_type}:"{search_term}" insubject:"{subject}"'
        books = get_books(query) # get_books function to fetch book data
            
    return render_template('results.html', books=books)

@app.route('/open_ebook/<isbn>/<subject>/<author>', methods=['GET'])
def open_ebook(isbn, subject, author):
    '''Loads a Jinja2 tempalte to create an HTML page for the ebook and opens it in a web browser.
    
    This function handles GET requests to the '/open_ebook/<isbn>/<subject>/<author>' URL.
    It uses the Jinja2 template engine to render an HTML page for the ebook based on the
    provided ISBN, subject, and author. The rendered HTML page is saved as a temporary file
    and opened in the default web browser. After opening the ebook, the function returns to
    the previous page.

    Args:
        isbn (str): The ISBN number of the ebook.
        subject (str): The subject of the ebook.
        author (str): The author of the ebook.

    Returns:
        str: Rendered HTML template string to return to the previous page.
    '''
    env = Environment(loader=FileSystemLoader('ebooks')) # creats Jinja2 environment object, configured to load templates (ebooks)
    template = env.get_template('google_ebook_reader_template.html')
    context = {'isbn': isbn} # dictionary for key-value pairs (isbn: corresponding value)
    rendered_template = template.render(context) # renders template with provided context
    temp_html_file = os.path.abspath(f'ebooks/{subject}_by_{author}_ebook.html') # saves rendered HTML to temp. file and opens in web
    with open(temp_html_file, 'w') as file:
        file.write(rendered_template)
    webbrowser.open('file://' + temp_html_file)
    
    # return to the previous page
    return render_template_string('''         
        <html><body><script>window.history.go(-1);</script></body></html>''')

def allowed_file(filename):
    '''Checks if the file extension is allowed (PDF).

    This function checks if the given filename has an allowed extension. It verifies
    that the file has an extension and that the extension is included in the ALLOWED_EXTENSIONS
    set.

    Args:
        filename (str): The name of the file to check.

    Returns:
        bool: True if the file has an allowed extension, False otherwise.
    '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_textbooks_info(syllabus_text):
    '''Extracts textbook information from the syllabus using GPT-3.

    This function uses OpenAI's GPT-3 model to extract textbook information from the given syllabus text.
    It constructs a query to extract details such as title, authors, publisher, edition, ISBN number,
    whether the textbook is required, and the subject. The function returns a list of dictionaries with
    the extracted information.

    Args:
        syllabus_text (str): The text of the syllabus from which to extract textbook information.

    Returns:
        list: A list of dictionaries containing textbook information, or None if an error occurs or no textbooks are found.

    Raises:
        Exception: If an error occurs during the API call or JSON decoding.

    Example:
        syllabus_text = "This course requires 'Physics of the Atmosphere and Climate' by Salby, M., B. Thamdrup..."
        textbooks_info = extract_textbooks_info(syllabus_text)
    '''

    client  = app.config["client"]

    query_text = '''Extract information about any textbooks mentioned in the syllabus. Extract title, authors. If you can also extract publisher, edition, ISBN number, if textbooks are required or not. Also try to derive what scientific discipline or subject that textbook belongs to. Create a list of dictionaries in JSON format, one for each textbook,  in this format (showing example(!) values): [{"title": "Physics of the Atmosphere and Climate", "authors": "Salby, M., B. Thamdrup", "publisher": "Cambridge University Press", "edition": "2012", "isbn": "978-0-12-415955-6", "required": true, "subject": "atmospheric science}, etc. ]. "required" must be either true or false. For missing dictionary values use the Json value null. If no textbooks are mentioned return "Error: not textbooks found". The syllabus text is as follows:\n ''' + syllabus_text

    # sends a request to OpenAI's API to generate a response from GPT-3 based on 'query_text'
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": query_text,
                    "max_tokens": 1500, # max words or parts of words it can generate
                    "temperature": 0.0, # super deterministic only
                }
            ],
            model="gpt-3.5-turbo",
        )   

        # choices is a list b/c we could request multiple answers but by default we only got 1 (which is fine)
        json_text = chat_completion.choices[0].message.content
    except Exception as e:
        print(e)
        return None
    
    # when AI returns "Error: no textbooks found"
    if "error" in json_text.lower():
        return None

    # convert the JSON text to a list of dictionaries
    try:
        textbooks_list = json.loads(json_text)
    except json.JSONDecodeError:
        return None

    # empty list to hold textbooks with all keys
    good_textbooks_list = []

    # check that we got all keys and if not fill with ""
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
    '''Handles the upload of a syllabus PDF and processes it to extract textbook information.

    This route handles both GET and POST requests. For POST requests, it processes the uploaded PDF syllabus file
    to extract textbook information. The function performs the following steps:
    1. Checks if a file is included in the request and if it has a valid filename.
    2. Saves the file to the specified upload folder.
    3. Extracts text from the uploaded PDF.
    4. Uses the extracted text to fetch textbook information through a text-processing function.
    5. Renders a results page with the extracted textbook information or an error message if no textbooks are found.

    Returns:
        Response: For GET requests, it renders the 'upload_syllabus.html' template for file upload.
                  For POST requests, it renders the 'syllabus_results.html' template with extracted textbook information.

    Example:
        POST request with a file:
        - If the file is valid and successfully processed, the response will be a rendered 'syllabus_results.html'
          page showing extracted textbook information.
        - If no textbooks are found or an error occurs during processing, the response will include a message indicating
          that no textbooks were found or an error occurred.

    Redirects:
        - If no file is provided or if the filename is empty, the function redirects back to the upload page.
    '''
    if request.method == 'POST':
        if 'syllabus_pdf' not in request.files: # check if form data includes a file with the key 'syllabus_pdf'
            return redirect(request.url)
        file = request.files['syllabus_pdf'] # retrieves uploaded file from the request
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename): # ensures file exists and has allowed extension
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename) # constructs a path to save the file in a specified folder
            file.save(file_path)

            # process uploaded syllabus PDF to extract textbooks
            # given that we know that the pdf location is valid 
            # this can't fail and will always return a string 
            text = process_syllabus(file_path)

            # debug: extract textbooks info from syllabus text using ChatGPT
            textbooks_info = extract_textbooks_info(text)

            if textbooks_info is None:
                textbooks_info = [{"title": "No textbooks found or error extracting textbook info."}]

            return render_template('syllabus_results.html', textbooks=textbooks_info)
    return render_template('upload_syllabus.html')

def process_syllabus(pdf):
    '''Extracts and cleans text from a PDF syllabus.

    This function takes the path to a PDF file, extracts its text content, and performs basic text cleaning.
    The cleaning process includes removing newlines and extra spaces to produce a continuous text string.

    Args:
        pdf (str): The file path to the PDF syllabus.

    Returns:
        str: A cleaned string of text extracted from the PDF syllabus.

    Logs:
        Prints the processing status of the PDF file and the extraction completion.
    '''
 
    print(f"Processing syllabus file: {pdf}")
    text = extract_text(pdf)

    # remove newlines, extra spaces, etc.
    text = " ".join(text.split())

    print("pdf extracted")
    return text

if __name__ == '__main__': # runs the Flask application
    app.run(debug=False, port=5000)

