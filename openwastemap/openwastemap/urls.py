"""OpenWasteMap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django_email_verification import urls as mail_urls

urlpatterns = [
    path("", include("map_viewer.urls"), name="home"),
    url(r"^admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("samples/", include("waste_samples.urls")),
    path("tiles/", include("tile_server.urls"), name="tiles"),
    path("email/", include(mail_urls)),
]