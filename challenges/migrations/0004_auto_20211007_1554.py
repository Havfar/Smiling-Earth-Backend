# Generated by Django 3.2.6 on 2021-10-07 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0003_alter_challengeuser_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='backgroundColor',
            field=models.CharField(default='ok', max_length=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='challenge',
            name='symbol',
            field=models.CharField(default='red', max_length=12),
            preserve_default=False,
        ),
    ]
