# Generated by Django 3.0.3 on 2020-04-25 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yohack_app', '0003_mentors_tg_account'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usr',
            name='questions',
        ),
        migrations.AddField(
            model_name='usr',
            name='usr',
            field=models.ManyToManyField(to='yohack_app.Questions'),
        ),
    ]