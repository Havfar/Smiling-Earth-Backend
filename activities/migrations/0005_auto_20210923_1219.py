# Generated by Django 3.2.6 on 2021-09-23 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0004_alter_activity_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='title',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterField(
            model_name='activitytag',
            name='title',
            field=models.TextField(max_length=200),
        ),
    ]
