from flask import Flask, render_template, request, redirect, url_for, render_template_string
import requests
import webbrowser
from jinja2 import Environment, FileSystemLoader
from get_ebooks_function import get_books  # CH was missing this import
import os

app = Flask(__name__) # will get imported by run_app.py

@app.route('/', methods=['GET'])
def index():
  #return render_template('search.html')
  return render_template('search_w_autocomplete.html')

@app.route('/search', methods=['POST'])  # cannot have 2 / routes
def perform_search():
  search_term = request.form['search_term']  # CH . was a /
  search_type = request.form['search_type']
  subject = request.form['subject'] 

  # CH as search_term could contain spaces it should be enclosed
  # in double quotes. Example: intitle:"The Great Gatsby"
  # B/c of that, I use ' for the f string
  query = f'{search_type}:"{search_term}" insubject:"{subject}"'  # 
  books = get_books(query)
  return render_template('results.html', books=books)

@app.route('/open_ebook/<isbn>/<subject>/<author>', methods=['GET']) # subject ws title in results.html
def open_ebook(isbn, subject, author): # was ibsn
  env = Environment(loader=FileSystemLoader('templates'))
  template = env.get_template('google_ebook_reader_template.html')
  context = {'isbn': isbn}
  rendered_template = template.render(context)
  temp_html_file = os.path.abspath(f'{subject}_by_{author}_ebook.html')
  with open(temp_html_file, 'w') as file:
    file.write(rendered_template)

  webbrowser.open('file://' + temp_html_file)  #  had _ instead of ) at the end
  #return redirect(url_for('index')) # CH was missing ) at the end of the line
  # trigger a javascript to go back to the previous page, which is the search results
  return render_template_string('''  
        <html><body><script>window.history.go(-1);</script></body></html>''')

app.run(debug=False, port=5000)

# AH tested and debugged app; shows on web browser and works with links
