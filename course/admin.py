from django.contrib import admin
from django.contrib.admin import ModelAdmin
from course.models import Course, Category, Contact


# Register your models here.
class CourseAdmin(ModelAdmin):
    list_display = ['title', 'category', 'views']
    search_fields = ['title', 'slug', 'body_text', 'category']
    list_filter = ['category']


class ContactAdmin(ModelAdmin):
    list_display = ['sno', 'name', 'email','phone']
    search_fields = ['sno', 'name', 'email']


admin.site.register(Course, CourseAdmin)
admin.site.register(Category)
admin.site.register(Contact,ContactAdmin)
