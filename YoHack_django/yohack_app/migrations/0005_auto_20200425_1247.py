# Generated by Django 3.0.3 on 2020-04-25 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yohack_app', '0004_auto_20200425_1247'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usr',
            name='usr',
        ),
        migrations.AddField(
            model_name='questions',
            name='usr',
            field=models.ManyToManyField(to='yohack_app.Usr'),
        ),
    ]
