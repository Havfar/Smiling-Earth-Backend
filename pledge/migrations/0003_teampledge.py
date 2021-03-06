# Generated by Django 3.2.6 on 2021-09-30 09:23

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_team_symbol'),
        ('pledge', '0002_rename_pledgeuser_userpledge'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamPledge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pledge', models.ForeignKey(on_delete=django.db.models.expressions.Case, related_name='pledge_team', to='pledge.pledge')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pledge_team', to='teams.team')),
            ],
        ),
    ]
