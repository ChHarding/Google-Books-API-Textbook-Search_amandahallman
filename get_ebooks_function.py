import requests

def get_books(query):
    url = "https://www.googleapis.com/books/v1/volumes"
    
    params = {
        "q": query,
        "maxResults": 40,
        "orderBy": "relevance",
        "langRestrict": "en"
    }

    try:
        # Makes the API request
        raw_response = requests.get(url, params=params)
        raw_response.raise_for_status()  # Raise an HTTPError on bad status
        
        items = raw_response.json()

        textbooks = []  # List to return the found textbooks
        if items['totalItems'] > 0:
            print(f"{items['totalItems']} books found")
            for book in items.get("items", []):
                volumeInfo = book.get("volumeInfo", {})
                category_list = volumeInfo.get("categories", ["None"])
                author = volumeInfo.get("authors", ["Unknown"])[0]
                description = volumeInfo.get("description", "No description")
                title = volumeInfo.get("title", "Unknown Title")
                isbn = None

                for identifier in volumeInfo.get("industryIdentifiers", []):
                    if identifier["type"] in ["ISBN_13", "ISBN_10"]:
                        isbn = identifier["identifier"]
                        break

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

# Testing the function
if __name__ == "__main__":
    print(get_books('intitle:"Linux system administration"')) 