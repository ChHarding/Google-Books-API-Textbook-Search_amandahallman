import requests

def get_books(query): # defines the function, which takes a single parameter 'query'.
    url = "https://www.googleapis.com/books/v1/volumes" # base URL for the Google Books API
    
    # dict to store query parameters for API request
    params = {
        "q": query,
        "maxResults": 40,
        "orderBy": "relevance",
        "langRestrict": "en"
    }

    try:
        # makes the API request
        raw_response = requests.get(url, params=params) # makes a GET request to the Google Books API with specified URL and parameters
        raw_response.raise_for_status()  #raise an HTTPError on bad status
        
        items = raw_response.json() # JSON response from API request parsed and stored in variable 'items'

        textbooks = []  # list to return the found textbooks
        if items['totalItems'] > 0:
            print(f"{items['totalItems']} books found")
            for book in items.get("items", []): # iterates through each book in the 'items["items"]' list, extract below information
                volumeInfo = book.get("volumeInfo", {})
                category_list = volumeInfo.get("categories", ["None"])
                author = volumeInfo.get("authors", ["Unknown"])[0]
                description = volumeInfo.get("description", "No description")
                title = volumeInfo.get("title", "Unknown Title")
                isbn = None
                
                # find ISBN, if found, assign 'isbn' variable, break loop
                for identifier in volumeInfo.get("industryIdentifiers", []):
                    if identifier["type"] in ["ISBN_13", "ISBN_10"]:
                        isbn = identifier["identifier"]
                        break
                # check if ISBN is available and if the book is available in EPUB format
                if isbn and book.get("accessInfo", {}).get("epub", {}).get("isAvailable", False):
                    textbooks.append({
                        "title": title,
                        "subject": ", ".join(category_list),
                        "author": author,
                        "description": description,
                        "isbn": isbn
                    })

        return textbooks

    except requests.exceptions.RequestException as e:
        print(f"Error fetching books: {e}")
        return []

# testing the function
if __name__ == "__main__":
    print(get_books('intitle:"Linux system administration"')) 