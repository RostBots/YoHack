"""YoHack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from yohack_app.views import *

urlpatterns = [
    path('',index),
    path('main_user', main_usr),
    path('main_mentor', main_mentor),
    path('reg_page',reg_page),
    path('enter', enter),
    path('log', log),
    path('reg', registr),
    path('logout', logut),
    path('create_question',create_question),
    path('questionPage',question),
    path('questionsPage', Question),
    path('answer',answers)
]
