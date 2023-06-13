"""abandone_object_detection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from detection import views
from django.conf.urls.static import static
from django.conf import settings

from detection.abandoned_object_detection.Abandoned_object_detection import detect_object

urlpatterns = [
    path("admin/", admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('', views.login_view, name='login'),
    path('detect/', views.abandoned_object_detection, name='abandoned_object_detection'),
    path('upload_video/', views.upload_video, name='upload_video'),
    path('abandoned_object_detection/', views.base, name='abandoned_object_detection'),
    path('documentation/', views.documentation, name='documentation'),
    # path('detect_object/', detect_object, name='detect_object'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

