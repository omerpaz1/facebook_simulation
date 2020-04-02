from django.contrib import admin
from .models import Post,Status,Friends,Friend_req

admin.site.register(Post)
admin.site.register(Status)
admin.site.register(Friends)
admin.site.register(Friend_req)
    