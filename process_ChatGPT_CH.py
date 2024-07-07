from API_keys import openai_api_key # format must be: openai_api_key = "123456789"
from openai import OpenAI
from pdfminer.high_level import extract_text # pip install pdfminer.six
import json
import os
from glob import glob
from pprint import pprint

def extract_textbook_from_syllabus(client, pdf):
    # convert pdf to text
    syllabus_text = extract_text(pdf)

    # remove newlines, extra spaces, etc.
    syllabus_text = " ".join(syllabus_text.split())

    # Call ChatGPT API to process the syllabus
    text_books = extract_textbooks(client, syllabus_text)
    return text_books

''' This is a slightly archaic form of the function. It's better to use the OpenAI Python library to make the API call. 
def call_chatgpt_api(text):
    # Use the OpenAI to get a response
    import openai   # CH imports go to the top of the file
    openai.api_key = 'your_openai_api_key'

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=text,
        max_tokens=1500
    )

    return response['choices'][0]['text']
'''
def extract_textbooks(client, syllabus_text):

    query_text = '''Extract any textbooks mentioned in the syllabus. Extract title, authors, publisher, edition, ISBN number, if they are required or not, and create a list of dictionaries in JSON format with this format: {"textbooks": [{"title": "Physics of the Atmosphere and Climate", "authors": "Salby, M., B. Thamdrup", "publisher": "Cambridge University Press", "edition": "2012", "isbn": "978-0-12-415955-6", "required": true}, etc. ]}. "required" must be either true or false. For missing dictionary values use the Json null. If no textbooks are mentioned return Error. The syllabus text is as follows: ''' + syllabus_text

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

    # convert the JSON text to a list of dictionaries
    try:
        textbooks_list = json.loads(json_text)
    except json.JSONDecodeError:
        return None
    
    return textbooks_list

def get_textbooks_from_syllabi(syllabus_folder):
    pdf_files = glob(syllabus_folder +   "/*.pdf")  
    textbooks_lst = []
    for pdf in pdf_files:
        pdf_file = os.path.basename(pdf) # get only the filename
        print("Textbooks for", pdf_file) # debug
        textbook_dict = {}
        textbook_dict["filename"] = pdf_file
        textbook_dict["textbooks"] = []
        textbooks = extract_textbook_from_syllabus(client, pdf)
        if textbooks is None:
            print("No textbooks found") # debug
            continue
        try:
            # check if any values are "null" and replace with None
            for textbook in textbooks["textbooks"]:
                for key, value in textbook.items():
                    if value == "null" or value == "Null":
                            textbook[key] = None
        except:
            continue # skip this textbook
        try:    
            for textbook in textbooks["textbooks"]:
                work_dict = {}
                for key, value in textbook.items():
                    work_dict[key] = value  # this is only so I can detect exceptions
                textbook_dict["textbooks"].append(work_dict)
        except:
            continue

        textbooks_lst.append(textbook_dict)
        
    return textbooks_lst
    
   


#
#  MAIN
#
client = OpenAI(
    api_key=openai_api_key # from API_keys.py
)

tl = get_textbooks_from_syllabi("syllabus_pdf")
for t in  tl:
    print(t["filename"])
    for textbook in t["textbooks"]:
        pprint(textbook) 

print()
print("All textbooks")
pprint(tl)