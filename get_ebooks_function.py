def get_books(query):
  url = "https://www.googleapis.com/books/v1/volumes 
  ### not sure if this (v1/volumes) is correct for my project - textbooks (based on class example)
  # parameters for the API request
  params = {
    "q": query,
    "maxResults": 40,
    "filter": "free-ebooks", ### double check this param ###
    "orderBy": "relevance"
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
    for books in items["items"]
      volumeInfo = book["volumeInfo"]
      subject = volumeInfo["subject"]
      author = volumeInfo.get("authors", ["Unknown])[0]
      description = volumeInfo.get("description", "No description")
      isbn = None
      for identifier in volumeInfo.get("industryIdentifiers", []):
        if identifier["type] in ["ISBN_13, "ISBN_10"]:
          isbn = identifier["identifier"]
          break

      if isbn:
        books.append({
          "subject": subject,
          "author": author,
          "description": description,
          "isbn": isbn
        })

  return books

# run the app
if __name__ == '__main__':
      app.run(debug=True)
