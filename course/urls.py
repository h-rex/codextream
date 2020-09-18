from django.urls import path
from django.views.generic import RedirectView

from course.views import contact, home, coursePost, search, category, CourseCategory, donate, privacy, team

urlpatterns = [
    path('course/', home, name='home'),
    path('course/<int:id>/<slug:slug>', coursePost, name='coursePost'),
    path('course/search/', search, name='search'),
    path('course/<str:query>', category, name='category'),
    path('course/categories/<int:pk>',CourseCategory.as_view(), name='course_category'),
    # path('course/<int:id>/<slug:slug>', CourseDetailView.as_view()),
   
    path('contact',contact,name='contact'),
    path('donate',donate,name='donate'),
    path('privacy',privacy,name='privacy'),
    path('team',team,name='team')
]
