# Generated by Django 3.1 on 2022-10-16 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_auto_20221014_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listitem',
            name='category',
            field=models.CharField(choices=[('House', 'House'), ('Building', 'Building'), ('NONE', 'NONE')], default='NONE', max_length=50),
        ),
    ]
