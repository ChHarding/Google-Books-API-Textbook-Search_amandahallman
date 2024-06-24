import requests


def get_books(query):
  url = "https://www.googleapis.com/books/v1/volumes" # CH was missing " at end
  ### not sure if this (v1/volumes) is correct for my project - textbooks (based on class example)
  # parameters for the API request
  params = {
    "q": query,
    "maxResults": 40,
    #"filter": "free-ebooks", ### double check this param ### CH commented out for testing as it will limit the results
    "orderBy": "relevance",  # CH was missing comma
    "langRestrict": "en"
  }

  # makes the API request
  raw_response = requests.get(url, params=params)

  if raw_response.status_code != 200:
    print(f"Error: {raw_response.status_code}")
    return []

  items = raw_response.json()

  textbooks = []                                  # will return a list of textbooks
  if items['totalItems'] > 0:
    print(f"{items['totalItems']} books found")
    for book in items["items"]: # CH was missing : and books needed to be book
      volumeInfo = book["volumeInfo"]

      # CH get the title from the volumeInfo

      category_list = volumeInfo.get("categories", ["None"]) # Google books API doesn't have subject)
      author = volumeInfo.get("authors", ["Unknown"])[0] # CH was missing " for "Unknown"  # maybe use multiple authors as with categories
      description = volumeInfo.get("description", "No description")
      isbn = None
      for identifier in volumeInfo.get("industryIdentifiers", []):
        if identifier["type"] in ["ISBN_13", "ISBN_10"]: # CH was missing " type" and "ISBN_10"
          isbn = identifier["identifier"]
          break
      
      # turn out we don't need to use the free ebook filter but we 
      # need to check that the book is available in epub format
      if isbn and book["accessInfo"]["epub"]["isAvailable"]:
        textbooks.append({  # CH was books
          "subject": ", ".join(category_list),  # convert list to string with comma separator
          "author": author,
          "description": description,
          "isbn": isbn
          # CH store the title of the book
        })
         

      
  return textbooks # CH was books # debugging code in VS - changed back to textbooks



# CH I moved the app start to textbook_search_app_CH.py
# below are some tests to make sure the function works
if __name__ == "__main__":
    print(get_books('intitle:"Linux system administration"')) 
    #print(get_books('inauthor:"Stepanek"')) 
    #print(get_books('inauthor:"Laura Townsend Kane" subject:"Information Science"'))
    #print(get_books('inauthor:"Laura Townsend Kane" subject:"Information Science"'))
    
# adding code to create a new branch and submit a pull request for Version 1 process report B
