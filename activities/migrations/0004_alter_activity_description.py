# Generated by Django 3.2.6 on 2021-08-24 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0003_auto_20210824_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
