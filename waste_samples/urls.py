"""
URLconf for the Waste Samples App.
"""

from django.urls import path

from . import views

app_name = 'waste_samples' # pylint: disable=invalid-name
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('new/', views.new_sample, name='create'),
]
