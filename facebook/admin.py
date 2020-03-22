from django.contrib import admin
from .models import Post,Comment,Status,Post_Comments

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Status)
admin.site.register(Post_Comments)