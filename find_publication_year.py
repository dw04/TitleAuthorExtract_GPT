import requests

def find_publication_year(title, author):
    url = "https://api.crossref.org/works"
    params = {
        "query.title": title,
        "query.author": author,
        "rows": 1
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    try:
        if data["status"] == "ok" and data["message"]["total-results"] > 0:
            paper = data["message"]["items"][0]
            return paper["published-print"]["date-parts"][0][0]
        else:
            return None
    except Exception as e:
        return None

if __name__ == "__main__":
    # Example usage
    title = "Localization with sliding window factor graphs on third-party maps for automated driving"
    author = "Wilbers"

    year = find_publication_year(title, author)
    if year:
        print(f"The publication year of '{title}' by {author} is {year}.")
    else:
        print("Publication not found.")
