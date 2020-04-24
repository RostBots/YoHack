import requests
from bs4 import BeautifulSoup

def get_answers(text):
    link = f'https://stackoverflow.com/search?q={"+".join(text.split())}&sort=votes'
    answer = requests.get(link)
    
    soup = BeautifulSoup(answer.text, 'html.parser')
    post = soup.find_all('a', {'class': 'question-hyperlink'})[:3]
    
    new_links = []
    names = []
    
    for elem in post:
        new_links.append('https://stackoverflow.com' + elem['href'])
        names.append(elem.text)
    
    return new_links, names
