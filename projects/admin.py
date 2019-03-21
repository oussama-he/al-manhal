from django.contrib import admin

from projects.models import Project, SecondaryObjective, Membership

admin.site.register(Project)
admin.site.register(SecondaryObjective)
admin.site.register(Membership)