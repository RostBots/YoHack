# Generated by Django 3.0.3 on 2020-04-25 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yohack_app', '0002_auto_20200424_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentors',
            name='tg_account',
            field=models.CharField(max_length=125, null=True),
        ),
    ]
