# Flask modules for creating the web application, rendering templates, handling requests, and performing redirects.
from flask import Flask, render_template, request, redirect, url_for, render_template_string
from werkzeug.utils import secure_filename
import requests
import webbrowser
from jinja2 import Environment, FileSystemLoader
# CH I would rename the fiel to get_ebooks.py and move it to the root folder
from old.get_ebooks_function import get_books  
import os

app = Flask(__name__) # will get imported by run_app.py (initializes the Flask application)

# Set the folder to store uploaded files
UPLOAD_FOLDER = '.'  # CH I cannot make it work with a different folder e.g. uploads 

ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])            # defines route for the homepage
def index():
  #return render_template('search.html')
  return render_template('search_w_autocomplete.html') # renders the 'search_w_autocomplete.html' template

@app.route('/search', methods=['POST'])     # defines a route for the search functionatlity ('/search')
def perform_search():
  search_term = request.form['search_term'] # extracts search term
  search_type = request.form['search_type'] # extracts search type
  subject = request.form['subject']         # extracts subject

  query = f'{search_type}:"{search_term}" insubject:"{subject}"'  # constructs query string for the book search
  books = get_books(query)                                        # calls the 'get_books' function with query
  return render_template('results.html', books=books)     # renders the 'results.html' template, passing the books to it

@app.route('/open_ebook/<isbn>/<subject>/<author>', methods=['GET']) # defines route to open an eBook using Google Books Embedded Viewer
def open_ebook(isbn, subject, author):                            
  env = Environment(loader=FileSystemLoader('templates'))           # creates Jinja2 environment and loads the
  template = env.get_template('google_ebook_reader_template.html')  # 'google_ebook_reader_template.html' template
  context = {'isbn': isbn}
  rendered_template = template.render(context)                      # renders template with provided ISBN
  temp_html_file = os.path.abspath(f'{subject}_by_{author}_ebook.html') # saves rendered template as HTML file
  with open(temp_html_file, 'w') as file:
    file.write(rendered_template)                                   # opens HTML file in the default web browser

  webbrowser.open('file://' + temp_html_file)
  # trigger a javascript to go back to the previous page, which is the search results
  return render_template_string('''         
        <html><body><script>window.history.go(-1);</script></body></html>''') 
        # returns HTML string with JavaScript to 
        # go back to previous page (search results)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_syllabus', methods=['POST'])
def upload_syllabus():
    # Check if the post request has the file part
    if 'syllabus_pdf' not in request.files:
        return redirect(request.url)
    file = request.files['syllabus_pdf']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File uploaded successfully'





app.run(debug=False, port=5000)           # runs the application

