# Generated by Django 3.1 on 2022-11-04 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0003_auto_20221017_0027'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='prediction',
            field=models.CharField(default='genuine', max_length=15),
        ),
    ]
