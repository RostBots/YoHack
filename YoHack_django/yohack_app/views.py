from django.shortcuts import render,get_object_or_404,redirect
from yohack_app.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import nltk
from nltk.corpus import stopwords
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import TweetTokenizer
import pandas as pd
import requests
from bs4 import BeautifulSoup


def preprocess(text):
    tokenizer = TweetTokenizer()
    return ' '.join(tokenizer.tokenize(text.lower()))


def check_question(text):
    data = pd.read_csv('yohack_app/questions.csv')
    data = data[5:]

    X = list(data['Question'].apply(preprocess))
    y = list(data['Answer'].apply(preprocess))

    X.append(text)
    y.append('')

    count_vect = CountVectorizer(max_features=5000)
    X_count = count_vect.fit_transform(X)

    clustering = DBSCAN(eps=2, min_samples=7)
    clustering.fit(X_count)

    clusters = clustering.labels_

    ans = {}
    for i in range(len(clusters) - 1):
        if clusters[i] == clusters[-1]:
            ans[X[i]] = y[i]

    return ans


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


def index(request):
    return redirect('/enter')


def enter(request):
    return render(request,'authorization.html')


def reg_page(request):
    cases = list(Case.objects.all())
    print('CASES',cases)
    if not cases:
        case = Case()
        case.name = 'Russian Hackers'
        case.save()
        case = Case()
        case.name = 'Some other case'
        case.save()
    cases = Case.objects.all()
    return render(request,'reg.html',{'cases':cases})


def main_usr(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        u = Usr.objects.get(user=user)
        cases = Case.objects.all()
        return render(request, 'main.html', {'questions' : u.questions.all(),'cases':cases})
    else:
        return redirect('/enter')


def main_mentor(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        u = Mentors.objects.get(user=user)
        print(u.case.id)
        questions = Questions.objects.filter(cases=u.case.id)
        print(questions)
        return render(request, 'main_mentor.html',{'questions':questions})
    else:
        return redirect('/enter')


def registr(request):
    log = request.GET.get('log', None)
    pwd = request.GET.get('pwd', None)
    is_mentor = request.GET.get('is_mentor', None)
    print('IS_MENTOR',is_mentor)
    case = request.GET.get('case',None)
    case = Case.objects.get(name=case)
    if log and pwd:
        print('########################')
        if User.objects.filter(username=log):
            messages.error(request, "Существует пользователь с таким логином.")
            return redirect('/enter')
        else:
            print('?????' * 10)
            user = User.objects.create_user(log)
            user.set_password(pwd)
            user.save()
            if is_mentor.lower() == 'да':
                ment = Mentors()
                ment.user = user
                ment.case = case
                ment.save()
                return redirect('/log')
            else:
                usr = Usr()
                usr.user = user
                usr.save()
                return redirect('/log')


def log(request):
    log = request.GET.get('log', None)
    pwd = request.GET.get('pwd', None)
    if log and pwd:
        user = authenticate(request, username=log, password=pwd)
        if user is not None:
            if Mentors.objects.filter(user=user):
               print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
               login(request, user)
               return redirect('/main_mentor')
            else:
                login(request, user)
                return redirect('/main_user')
        else:
            # messages.info("неверный логин или пароль")
            return redirect('/enter')
    return redirect('/enter')


def logut(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/enter')
    else:
        return redirect('/enter')


def create_question(request):
    name = request.GET.get('name',None)
    text = request.GET.get('text',None)
    case = request.GET.get('case',None)
    case = get_object_or_404(Case,pk=2)
    for_mentor = request.GET.get('for_mentor',None)
    if (text != None) and (case != None) and (for_mentor == None):
        new_question = Questions()
        new_question.name = name
        new_question.text = text
        new_question.cases = case
        print(new_question.cases)
        new_question.save()
        new_question_id = Questions.objects.get(name=new_question.name)
        user = User.objects.get(username=request.user)
        u = Usr.objects.get(user=user)
        u.questions.add(new_question_id.id)
        u.save()
    elif (for_mentor != None):
        mentors = Mentors.objects.filter(case=case)
        return render(request,'tg_page.html',{'mentors': mentors})
    return redirect('/main_user')


def question(request):
    if request.user.is_authenticated:
        question_id = request.GET.get('id', None)
        question = get_object_or_404(Questions, pk=question_id)
        user = User.objects.get(username=request.user)
        u = Mentors.objects.get(user=user)
        questions = Questions.objects.filter(cases=u.case)
        return render(request, 'main_mentor.html',{'questions':questions,'current_question': question})
    else:
        return redirect('/enter')
    return redirect('/')


def answers(request):
    answer = request.GET.get('answ',None)
    text = request.GET.get('text',None)
    print(text,answer)
    if (text != None) and (answer != None):
        questioN = Questions.objects.get(text=text)
        print(questioN)
        questioN.answer = answer
        questioN.save()
    return redirect ('/main_mentor')


def Question(request):
    if request.user.is_authenticated:
        question_id = request.GET.get('id', None)
        question = get_object_or_404(Questions, pk=question_id)
        user = User.objects.get(username=request.user)
        u = Usr.objects.get(user=user)
        questions = list(u.questions.all())
        similars = check_question(question.text)
        Texts = []
        for key,value in similars.items():
            Texts.append([key,value])
        Texts = Texts[:5]
        return render(request, 'question.html', {'current_question': question,'txt':Texts})
    else:
        return redirect('/enter')
    return redirect('/')



