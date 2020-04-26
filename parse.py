import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_answers(text):
    i = 6
    for kp in range(10):
        link = f'https://stackoverflow.com/search?page={kp + 1}&pagesize=50&q={"+".join(text.split())}&sort=answers'
        answer = requests.get(link)

        soup = BeautifulSoup(answer.text, 'html.parser')
        post = soup.find_all('a', {'class': 'question-hyperlink'})

        questions = []
        answers = []

        for elem in post:
            try:
                questions.append(elem.text)
                answers.append(" ".join(BeautifulSoup(requests.get('https://stackoverflow.com' + elem['href']).text, 'html.parser').find_all('div', {'class': 'answer'})[0].text.split()))

                print(1)
                data.loc[i] = [questions[-1], answers[-1]]
                i += 1
                print(2)
            except Exception as e:
                print(e)

data = pd.read_csv('questions.csv')
data = data[["Question","Answer"]]
get_answers(*кидай сюда вопрос*)
data.to_csv("questions.csv")