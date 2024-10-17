from django.urls import path

from cases.views import transcribed_cases_count

from .views import (
    TranscriptionViewSet,
    # TranscriptionDetailView,
    DiarizedSegmentListCreateView,
    DiarizationDetailView,
    AudioChunkViewSet
)

urlpatterns = [
    path('transcribed-cases/', transcribed_cases_count, name='transcribed-cases'),

        path('transcriptions/', TranscriptionViewSet.as_view({'get': 'list', 'post': 'create'}), name='transcription-list'),
    path('transcription/<int:pk>/', TranscriptionViewSet.as_view({'get': 'retrieve'}), name='transcription-detail'),

    # Diarization API paths
    path('diarizations/', DiarizedSegmentListCreateView.as_view(), name='diarized-segment-list-create'),
    path('diarization/<int:pk>/', DiarizationDetailView.as_view(), name='diarized-detail'),

    path('audio-chunks/', AudioChunkViewSet.as_view({'get': 'list', 'post': 'create'}), name='audio-chunk-list-create'),
    path('audio-chunks/<int:pk>/', AudioChunkViewSet.as_view({'get': 'retrieve'}), name='audio-chunk-detail'),
]