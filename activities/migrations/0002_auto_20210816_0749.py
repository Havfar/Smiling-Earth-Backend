# Generated by Django 3.2.6 on 2021-08-16 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='type',
        ),
        migrations.AddField(
            model_name='activity',
            name='activity_enum_value',
            field=models.IntegerField(default=1),
        ),
    ]