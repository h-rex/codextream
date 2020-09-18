from django.contrib import admin
from django.contrib.admin import ModelAdmin

from blog.models import Post, CategoryBlog ,Comment, SubCommnet

class CommentAdmin(ModelAdmin):
    list_display = ['user', 'time', 'post']
    search_fields = ['user', 'time', 'post']

# Register your models here.
admin.site.register(Post)
admin.site.register(CategoryBlog)
admin.site.register(Comment ,CommentAdmin)
admin.site.register(SubCommnet)
