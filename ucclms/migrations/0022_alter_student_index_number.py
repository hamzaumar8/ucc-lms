# Generated by Django 3.2.6 on 2021-10-21 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ucclms', '0021_book_no_stolen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='index_number',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
