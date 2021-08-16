from django.contrib import admin
from teams.models import Member, Team

admin.site.register(Team)
admin.site.register(Member)