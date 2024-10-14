# urls.py
from django.urls import path

from cases.views import transcribed_cases_count


urlpatterns = [
    path('api/transcribed-cases/', transcribed_cases_count, name='transcribed-cases'),
]
