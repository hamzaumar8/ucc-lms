# Generated by Django 3.2 on 2021-08-02 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ucclms', '0002_auto_20210802_1943'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='author',
            new_name='name',
        ),
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.ManyToManyField(blank=True, to='ucclms.Author'),
        ),
    ]
