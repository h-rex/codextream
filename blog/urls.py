from django.urls import path
from django.views.generic import RedirectView

from blog.views import blogHome, blogPost, list_of_post_by_category, blogSearch

urlpatterns = [
    path('', blogHome, name='blogHome'),
    path('<str:slug>', blogPost, name='blogPost'),
    path('category/<slug>/', list_of_post_by_category, name='list_of_post_by_category'),
    path('search/', blogSearch, name='blogSearch'),
]
