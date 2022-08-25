"""Geolocation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from .views import track_material, track_person, view_analytics, track_specific_person, track_specific_material

urlpatterns = [
    path('track_material', track_material, name='track_material'),
    path('track_person', track_person, name='track_person'),
    path('track_specific_person/<name>', track_specific_person, name='track_specific_person'),
    path('track_specific_material', track_specific_material, name="track_specific_material"),
    path('analytics', view_analytics, name='analytics')
]
