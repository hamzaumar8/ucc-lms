# Generated by Django 3.2 on 2021-08-02 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ucclms', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='address',
            new_name='publisher',
        ),
        migrations.RemoveField(
            model_name='book',
            name='mobile_number',
        ),
        migrations.AddField(
            model_name='book',
            name='availability',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
