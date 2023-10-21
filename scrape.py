import requests
from bs4 import BeautifulSoup


if __name__ == "__main__":
    response = requests.get("https://www.english-for-students.com/Words-by-Theme.html")
    if response.status_code != 200:
        raise ValueError()
    
    soup = BeautifulSoup(response.content, features="html.parser")
    table = soup.find_all("ol")[0]
    table_links = table.find_all("a")

    category_lists = {}

    for table_link in table_links:
        print(table_link.text)

        category_lists[table_link.text] = []


        response = requests(table_link["href"])
        if response.status_code != 200:
            raise ValueError()
        
        break
    
    print(table_elements[0])
    print(table_elements[0]["href"])
