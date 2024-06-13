# Amanda-Hallman-Project-Spec
Project spec for HCI 584 based on recommending textbook or book information relevant to college or university courses and syllabi.

### General description of the project
Flask web interface that finds textbooks or books related to a university or college course using:

- Google Books API: https://developers.google.com/books/docs/v1/using

The interface will have a search bar, filter, and output area. The main interaction will be a user searching for a course subject 
(i.e., Math, Biology, Human-Computer Interaction), in which the system produces a list of relevant textbooks or books based on what was inputted. The user will be able to select a link associated with a textbook that 
brings them to where they can purchase, rent, or check out the book. There will be a loop that allows the user to continue searching without having to leave the application.

The general interface [after the user has logged in] will be a web application (browser) using Flask, but I would start with a jupyter notebook. The application will have a search bar located at the top 
of the page, the user's profile in the upper-right corner of the page, and recommended books categorized by subject shown in the center of the application.  The user should be able to filter/refine the search parameters by setting the date, subject, 
type (textbook or book), and/or author. By default, the most popular (or purchased, used, etc.) books from 1990 - present would be shown.

The primary stakeholders of this application will be college or university students taking courses, and the secondary stakeholders will be college or university faculty members who want 
additional resources for their courses or the general public. A problem that it will help solve is the limitation of resources provided by the instructor and the course. Students could find further resources 
(i.e., books or textbooks) that were not provided by the instructor but could be helpful. Students [or the general public] could use it to find books related to a subject that piques their interest, 
such as a friend or expert recommending a book to you that has helped them in a subject or that is merely interesting.

### Task Vignettes (User activity "flow")
- Task 1: Search for "biology" textbooks
- Task 2: Filter by date and type
- Task 3: Find where to purchase, rent, or check out
  
  - User configurable fields:
    - date range: default 1990 to current, only uses years
    - subject: default to all
    - type: default to both (textbooks or books)
    - author: default to all

The user opens the application in the browser and begins on the homepage. The homepage, by default, recommends popular, possibly irrelevant, books or textbooks in the center of the page in a grid-like 
fashion (ideally showing a picture). The user will use the search bar at the top of the page to type the subject "biology". The user will hit 'enter', which connects to the API and produces a list of 
recommended books or textbooks to the user related to biology. The user then changes the filter to show only textbooks and changes the date range from 2014 to present. With "biology" still in the search bar, 
the user will hit 'enter' again and be shown a new list of related textbooks from 2014 - present. After finding a book that matches what they are looking for, they will select the link next to the textbook,
which will take them to where they can purchase, rent, or check out the textbook (i.e., Amazon, local library, etc.). 

### Technical "flow"

Data structures:

- Amazon API or Open Library Search API
- a dict or object that stores all current values for search filters: date range, subject, type, author
- a list to store text from syllabi and to generate keywords
- for loops for text in PDF or Word Documents

Core functions:

- def extract_text_from_pdf(file_path):
  - takes a file path to a PDF and extracts the text from each page
  - possibly using PyMuPDF?
  - extracted text is concatenated and returned

- def extract_text_from_docx(file_path):
  - takes a file path to a DOCX file and extracts the text from each paragraph
  - possibly using python-docx?
  - extracted text is concatenated and returned
    
- def extract_keywords(text):
  - function to process the text and extract keywords
  - possibly using NLP model spaCy?
  - tokenizes the text and filters out non-alphabetic tokens and stop words
  - returns a list of keywords

- def upload_syllabus():
  - handles the file upload from the user
  - checks file extension to determine if PDF or DOCX
  - calls appropriate text extraction function
  - extracted text is processed to get keywords to use to search for books using API

- def search_amazon_books(keywords)
  - placeholder function represents where to implement the logic to search for books using Amazon API (or Open Library Search API) based on extracted keywords
  - return a list of book details

- def get_filter_data(date_range, subject, type, author)
  - scrapes data from API according to arguments
  - filters can be none or unchanged

Program flow:

- Flask app main page creates the GUI, with search bar, filters, and file upload icon
- file handling and parsing through Flask server (syllabi)
- text and keyword extraction
- HTML and Jinja2 to display book details?
- changes in GUI fields are collected in an HTML form? and sent back to the user
- scrapes a new dataframe according to user values, clears results, and produces a new list
- unsupported file format produces error message

### Final (self) assessment

- Figuring out the core prototype first based on my sketch and then thinking about enhancements (i.e., uploading syllabi) and how to add that as an additional feature
- I feel somewhat confident in implementing the spec as is but I would need help with figuring out what tools to use (Flask, APIs, Bootstrap, Folium, etc.).
- If it's possible to use Amazon API or Open Search Library API for the intended goal, figuring out how to include the filter data (such as all subjects and authors), and whether
it's possible to display this on a GUI. I also don't know if the application can bring up where to rent or check out the book instead of just purchasing on Amazon.
- The parts I am least familiar with are the tools to use (Flask, Bootstrap, Folum, etc.) and how they specifically work. I have worked with Flask in HCI 574, but that was my first introduction.
