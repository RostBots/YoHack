from django.db import models
from django.contrib.auth.models import User


class Case(models.Model):
    name = models.CharField(max_length=125, null=True)


class Mentors(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, null=True)
    tg_account = models.CharField(max_length=125, null=True)


class Questions(models.Model):
    name = models.CharField(max_length=125, null=True)
    text = models.TextField(null=True)
    cases = models.ForeignKey(Case, on_delete=models.CASCADE, null=True)
    answer = models.TextField(null=True)


class Usr(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    questions = models.ManyToManyField(Questions)







