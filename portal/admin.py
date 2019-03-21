from django.contrib import admin

from portal.models import Publication, Comment, Rating

admin.site.register(Publication)
admin.site.register(Comment)
admin.site.register(Rating)
