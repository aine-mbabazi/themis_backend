# urls.py
# from django.urls import path

# from cases.views import transcribed_cases_count


from django.urls import path
from api.views import TranscriptionViewSet


urlpatterns = [
    # path('transcriptions/transcription_status_counts/', TranscriptionViewSet.as_view({'get': 'transcription_status_counts'}), name='transcription-status-counts'),

]
