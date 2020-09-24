"""codextream URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from codextream import settings

admin.site.site_header = "CodeXtream Admin"
admin.site.site_title = "CodeXtream Admin Panel"
admin.site.index_title = "Welcome to CodeXtream Admin Panel"

urlpatterns = [
                  path('heypajxn/', admin.site.urls),
                  path('', include('course.urls')),
                  path('blog/', include('blog.urls')),
                  path('freepdf/', include('freepdf.urls')),
                  path('blog/', RedirectView.as_view(url='blog/')),
                  path('freepdf/', RedirectView.as_view(url='freepdf/')),
                  path('ckeditor/', include('ckeditor_uploader.urls')),
                  path('', RedirectView.as_view(url='course/')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
