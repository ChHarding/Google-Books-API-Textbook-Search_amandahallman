# OpenAI API Textbook Search - Developer's Guide

### Overview
This application is a web-based tool designed for users to search for textbooks by subject, title, or author. It is also designed for uploading PDF syllabi, extracting textbook information using OpenAI's GPT-3, and presenting the results to the user. It leverages Flask for web server management, Jinja2 for templating, and PDFMinder for PDF text extraction. The application also integrates with the OpenAI API to analyze and process the text from the syllabus.

### Key Components

- Flask Web Framework
    - Manages HTTP requests and responses, routes URLs to appropriate functions, and serves HTML templates.
- Jinja2 Templating
    - Used for rendering HTML templates dynamically based on context data.
- PDFMiner
    - Extracts text from PDF files uploaded by users.
- OpenAI API
    - Provides AI-based analysis to extract textbook information from syllabus text.
- Werkzeug
    - Provides utilities for file handling, such as securing file names.

### Directory Structure

/Google-Books-API-Textbook-Search_amandahallman
│
├── /ebooks
│   ├── google_ebook_reader_template.html     # Jinja2 template for rendering ebook pages
│
├── /uploads
│   └── [uploaded PDF files]                  # Directory where uploaded files will be saved
│
├── /static
│   ├── /css                                  # Directory for CSS files
│
├── /old                                      # Folder containing old files/folders for reference                                   
│
├── /templates
│   ├── search_w_autocomplete.html            # Template for the main search page with autocomplete
│   ├── results.html                          # Template for displaying search results
│   ├── upload_syllabus.html                  # Template for the syllabus upload page
│   └── syllabus_results.html                 # Template for displaying extracted textbook info
│
├── get_ebooks_function.py                    # Script with the 'get_books' function
├── api_key.py                                # File containing the OpenAI API key
├── main.py                                   # Main application script
└── bugs.txt                                  # File listing possible bugs

### Install/Deployment/Admin Issues

- Environmental Variables: ensure that 'api_key.py' is properly configured with YOUR OpenAI API key.
    - Example: openai_api_key = "your_openai_api_key_here"

- File Permissions and Uploads: ensure that the '/uploads' directory exists and has the appropriate permissions for file uploads.

- Security: ensure that sensitive information (i.e., API keys, credentials) is not exposed.

### User Interaction and Flow Walkthrough

1. Landing on the search page: the user lands on the main search page where they can search for textbooks or upload a syllabus.
2. Performing a search: the user submits search parameters (subject, title, and/or author) to find textbooks.
3. Viewing search results: the search results are displayed to the user.
4. Opening a textbook: the user can view details of a selected book in the browser (eBook, Google Play, Amazon)
5. Uploading a syllabus: the user uploads a PDF syllabus for textbook extraction.
6. Viewing textbook information: the extracted textbook information is displayed based on the syllabus. 

### Detailed Flow and Code Involvement

1. Landing on the search page
    - User Action: the user navigates to the rool URL ('/').
    - Code Involvement:
        - Function: 'index()' (located in the main module)
            - Handles GET requests to render the 'search_w_autocomplete.html' template, which includes a form for users to enter search criteria and perform textbook searches

![img](<Screenshot 2024-07-24 at 1.25.53 PM.png>)

2. Performing a search
    - User Action: the user submits a search form with parameters for search term, type, authors, subject, or ISBN. 
    - Code Involvement:
        - Function: 'perform_search()' (located in the main module)
            - Handles POST requests to /search. Constructs a query based on the form data and calls get_books() from get_ebooks_function.py to fetch book data.
        - Function: 'get_books(query)' (located in 'get_ebooks_function.py')
            - Fetches book data based on the constructed query. The results are passed to the results.html template.

3. Viewing search results:
    - User Action: the user views the search results displayed on the results page.
    - Code Involvement:
        - Template: 'results.html'
            - Renders the book search results based on the data received from the perform_search() function.

4. Opening a textbook:
    - User Action: the user clicks on a link to open an eBook, Google Play, or Amazon
    - Code Involvement:
        - Function: 'open_ebook(isbn, subject, author)' (located in the main module)
        - Template: 'google_ebook_reader_template.html' (loaded from the 'ebooks' directory)
            - Handles GET requests to /open_ebook/<isbn>/<subject>/<author>. Renders the google_ebook_reader_template.html using Jinja2 and opens it in the browser.

5. Uploading a syllabus:
    - User Action: the user uploads a PDF syllabus file.
    - Code Involvement:
        - Function: 'upload_syllabus()' (located in the main module)
            - Handles both GET and POST requests to /upload_syllabus. For POST requests, it saves the uploaded PDF, extracts text using process_syllabus(), and then calls extract_textbooks_info() to get textbook data.
        - Function: 'process_syllabus(pdf)' (located in the main module)
            - Extracts and cleans text from the uploaded PDF.
        - Function: 'extract_textbooks_info(syllabus_text)' (located in the main module)
            - Uses OpenAI's GPT-3 model to extract textbook information from the syllabus text. It returns a list of dictionaries with textbook details or an error message.

6. Viewing textbook information:
    - User Action: the users views the extracted textbook information from the syllabus.
    - Code Involvement:
        - Template: 'syllabus_results.html'
            - Displays the extracted textbook information based on the data provided by extract_textbooks_info().




