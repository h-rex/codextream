from django.urls import path
from freepdf.views import home, pdfPost, pdfCategory, pdfSearch

urlpatterns = [
    path('', home, name='freepdf'),
    path('<str:slug>', pdfPost, name='pdfPost'),
    path('category/<slug:slug>/', pdfCategory, name='category_pdf'),
    path('search/', pdfSearch, name='pdfSearch'),
]
