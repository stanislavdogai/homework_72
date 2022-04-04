from django.urls import path

from webapp.views import home

app_name = 'webapp'

urlpatterns = [
    path('', home, name='index')
]