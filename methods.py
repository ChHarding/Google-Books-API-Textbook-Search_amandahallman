from flask import Flask, render_template, request, redirect, url_for
import requests
import webbrowser
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('search.html')

@app.route('/')
def search():
  search_term = request/form['search_term']
  search_type = request/form['search_type']
  query = f"{search_type}:{search term}"
  books = get_books(query)
  return render_template('results.html', books=books)

@app.route('/open_ebook/<isbn>/<subject>/<author>')
def open_ebook(ibsn, subject, author):
  env = Environment(loader=FileSystemLoader('templates'))
  template = env.get_template('google_ebook_reader_template.html')
  context = {'isbn': isbn}
  rendered_template = template.render(context)
  temp_html_file = f'{subject}_by_{author}_ebook.html

  with open(temp_html_file, 'w') as file:
    file.write(rendered_template)

  webbrowser.open(temp_html_file_
  return redirect(url_for('index')
