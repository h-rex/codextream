from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from freepdf.models import Pdf, CategoryPdf


class PdfAdmin(ModelAdmin):
    list_display = ['title', 'category_pdf']
    search_fields = ['title', 'slug', 'category_pdf']
    list_filter = ['category_pdf']


admin.site.register(Pdf, PdfAdmin)
admin.site.register(CategoryPdf)
