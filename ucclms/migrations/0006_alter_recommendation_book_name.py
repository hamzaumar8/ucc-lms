# Generated by Django 3.2 on 2021-08-02 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ucclms', '0005_auto_20210802_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendation',
            name='book_name',
            field=models.CharField(max_length=255),
        ),
    ]
