# OpenAI API Textbook Search - User Guide
The OpenAI API Textbook app helps you find textbooks and extract textbook information from syllabus PDFs. You can search for books by title, author, or ISBN, and upload syllabus PDFs to automatically identify and list required textbooks.

### General description of the application
This app is a web-based tool designed for users to search for textbooks by subject, title, or author. It is also designed for uploading PDF syllabi, extracting textbook information using OpenAI's GPT-3, and presenting the results to the user. It leverages Flask for web server management, Jinja2 for templating, and PDFMinder for PDF text extraction. The application also integrates with the OpenAI API to analyze and process the text from the syllabus.

- OpenAI API: https://openai.com/api/

### Set up: 

1. Configure API Keys

  - Obtain OpenAI API key: sign up for OpenAI API access at OpenAI: https://beta.openai.com/signup/. After signing up, you'll receive an API key under Profile > API reference.

  - Create a 'api_key.py' file in the project root directory with the following context:
    - openai_api_key = "your_openai_api_key_here" (Replace 'your_openai_api_key_here' with your actual OpenAI API key).

2. Start the Flask application

  - Open your web browser and go to 'http://127.0.0.1:5000' to access the application.

### Using the Application:

1. Search for textbooks:

  - On the main page, enter search parameters for the desired textbook (title, author, subject, ISBN) and submit the search form.
  - The application will display search results based on the entered criteria.

  ![img](docs/Homepage.png)

  ![img](<docs/Homepage w: input.png>)

  ![img](<docs/Search results.png>)

2. View eBook:

  - Click the blue link, 'Open Ebook', to view detailed information.
  - The application will open a new HTML page with the eBook in your default web browser.
    - Possible error: the textbook selected does not have an eBook option.
  
  ![img](<docs/eBook reader.png>)

3. View Google Play:

  - Click the blue link, 'View on Google Play', to view detailed information.
  - The application will open a new HTML page with the eBook in your default web browser.
    - Possible error: the textbook selected does not have the option for Google Play.
  
  ![img](<docs/Google Play.png>)

4. View Amazon:

  - Click the blue link, 'View on Amazon', to view detailed information.
  - The application will open a new HTML page with the eBook in your default web browser.
    - Possible error: the textbook selected does not have the option to purchase on Amazon.

  ![img](docs/Amazon.png)

5. Upload a syllabus:

  - Back on the main page, select the 'Choose File' button to pull a syllabus from local files. Once selected, click 'Upload Syllabus'.
  - The application will proccess the PDF, extract textbook information, and display the results.

  ![img](<docs/Syllabi Input.png>)

  ![img](<docs/Syllabus upload.png>)

### User Interaction Summary

1. Landing on the search page: the user lands on the main search page where they can search for textbooks or upload a syllabus.
2. Performing a search: the user submits search parameters (subject, title, and/or author) to find textbooks.
3. Viewing search results: the search results are displayed to the user.
4. Opening a textbook: the user can view details of a selected book in the browser (eBook, Google Play, Amazon)
5. Uploading a syllabus: the user uploads a PDF syllabus for textbook extraction.
6. Viewing textbook information: the extracted textbook information is displayed based on the syllabus.



![HCI 584 Project GIF](https://github.com/amandahallman/Google-Books-API-Textbook-Search_amandahallman/blob/main/HCI%20584%20Project%20GIF.gif)
