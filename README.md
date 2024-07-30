# Google/OpenAI API Textbook Search - User Guide

The Google & OpenAI API Textbook app is a simple tool designed for finding textbooks based on search query, uploading PDF syllabi, extracting textbook information, and presenting a list of results. It can be used for simplified textbook searches with an easy-to-use interface, automated textbook extraction when given course syllabi, and to streamline workflow for educators, students and researchers. In addition, the tool can be used to read textbooks on an eReader or purchase the textbooks on Google Play or Amazon.

This guide establishes how to set up the app and provides instructions on how to use it. It is important that the repository has already been downloaded or cloned to your local machine. **NOTE:** **The provided instructions are for macOS.**

- Google Books API: https://www.googleapis.com/books/v1/volumes
- OpenAI API: https://openai.com/api/


![HCI 584 Project GIF](https://github.com/amandahallman/Google-Books-API-Textbook-Search_amandahallman/blob/main/docs/HCI%20584%20Project%20GIF.gif)


## Setting Up the Application: 

### Configure OpenAI API Key:

1. Obtain OpenAI API key: sign up for OpenAI API access at OpenAI: https://beta.openai.com/signup/. After signing up, you'll receive an API key under 'Your profile' in the top right of the page, then User API keys.

2. Select '+ Create new secret key'. Copy your new key.

3. Next, create a python file in the project root directory called 'api_key.py' with the following context:
  
**openai_api_key = "your_openai_api_key_here"** (replace 'your_openai_api_key_here' with your actual OpenAI API key).
  
![img](<docs/api key.png>)
  
  **NOTE:** **Do not share your API key with anyone.** It can be misused if shared or stolen.

### Install required packages (Python >= 3.10):

  Run the following commands via command line interface (CLI). To open a command line, select 'Terminal' in the menu bar, then 'New Terminal'.

  1. `pip3 install Flask --upgrade`
  2. `pip3 install requests --upgrade`
  3. `pip3 install jinja2 --upgrade`
  4. `pip3 install pdfminer.six --upgrade`
  5. `pip3 install openai --upgrade`
  6. `pip3 install werkzeug --upgrade`

  These commands can also be found in requirements.txt.

## Running the Application:

  To access the Flask application, go to the root folder (cd), and either: run it through an IDE, right click `main.py` and select Open with - Python Launcher.app, or via command line interface (CLI).

  To access the application via CLI, follow the instructions below:
  
  1. Open a command line via 'Terminal' in the menu bar, then 'New Terminal'
  
  2. Type `python3 main.py` and press enter to start the application.
  
  3. Command click `http://127.0.0.1:5000`. This is the URL to the Flask application.

![img](<docs/Running-app.png>)

## Using the Application:

### Search for textbooks:

  - On the main page, enter search parameters for the desired textbook (title, author, subject, ISBN).
  - **Optional:** In addition to title, author, or ISBN, search for specific subject via the 'Subject' drop-down menu to narrow down results.
  - Select the 'by Title' or 'by Author' button to search for the textbook.
  - The application will display search results based on the entered criteria.

  ![img](docs/Homepage.png)

  ![img](<docs/Homepage w: input.png>)

  ![img](<docs/Subject drop-down.png>)

  ![img](<docs/Search results.png>)

### View eBook:

  - Click the blue link, 'Open Ebook', to view detailed information.
  - The application will open a new HTML page with the eBook in your default web browser.
    - Possible error: the textbook selected does not have an eBook option.
  
  ![img](<docs/eBook reader.png>)

### View on Google Play:

  - Click the blue link, 'View on Google Play', to view detailed information.
  - The application will open a new HTML page with the eBook in your default web browser.
    - Possible error: the textbook selected does not have the option for Google Play.
  
  ![img](<docs/Google Play.png>)

### View on Amazon:

  - Click the blue link, 'View on Amazon', to view detailed information.
  - The application will open a new HTML page with the eBook in your default web browser.
    - Possible error: the textbook selected does not have the option to purchase on Amazon.

  ![img](docs/Amazon.png)

### Upload a syllabus:

  - Back on the main page, select the 'Choose File' button to pull a syllabus from local files. Once selected, click 'Upload Syllabus'.
  - The application will proccess the PDF, extract textbook information, and display the results. Select 'Search for selected textbook' for viewing options.

  ![img](<docs/Syllabi Input.png>)

  ![img](<docs/Syllabus upload.png>)

## User Interaction Summary

1. Landing on the search page: the user lands on the main search page where they can search for textbooks or upload a syllabus.
2. Performing a search: the user submits search parameters (subject, title, and/or author) to find textbooks.
3. Viewing search results: the search results are displayed to the user.
4. Opening a textbook: the user can view details of a selected book in the browser (eBook, Google Play, Amazon)
5. Uploading a syllabus: the user uploads a PDF syllabus for textbook extraction.
6. Viewing textbook information: the extracted textbook information is displayed based on the syllabus.

## Possible Bugs

- Unable to search for selected textbook after syllabus upload; no results found
  - Potential fix: Searching for the textbook(s) by title or author
- Separate tab for eBook, Google Play, Amazon
  - Potential fix: The user must close out of the additional tab
- No results based on search parameters
  - Potential fix: Try new search parameters
- Errors in typed words
  - Potential fix: retype the exact book title or author



**NOTE:** **Developer's Guide in docs folder.**