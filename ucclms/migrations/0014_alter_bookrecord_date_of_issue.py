# Generated by Django 3.2.6 on 2021-10-02 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ucclms', '0013_administrator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookrecord',
            name='date_of_issue',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
