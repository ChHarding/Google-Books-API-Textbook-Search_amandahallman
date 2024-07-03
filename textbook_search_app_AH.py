# Flask modules for creating the web application, rendering templates, handling requests, and performing redirects.
from flask import Flask, render_template, request, redirect, url_for, render_template_string
import requests
import webbrowser
from jinja2 import Environment, FileSystemLoader
from old.get_ebooks_function import get_books
import os

app = Flask(__name__) # will get imported by run_app.py (initializes the Flask application)

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
        <html><body><script>window.history.go(-1);</script></body></html>''') # returns HTML string with JavaScript to
                                                                            # go back to previous page (search results)

app.run(debug=False, port=5000)           # runs the application

