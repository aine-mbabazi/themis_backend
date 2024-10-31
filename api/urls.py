from django.urls import path

from .views import (
    TranscriptionViewSet,
    # TranscriptionDetailView,
    DiarizedSegmentListCreateView,
    DiarizationDetailView,
    AudioChunkViewSet,
    CaseMatchingDetailView,
    CaseMatchingListView,
)

urlpatterns = [

    path('transcriptions/', TranscriptionViewSet.as_view({'get': 'list', 'post': 'create'}), name='transcription-list'),
    path('transcription/<int:pk>/', TranscriptionViewSet.as_view({'get': 'retrieve'}), name='transcription-detail'),

    # Diarization API paths
    path('diarizations/', DiarizedSegmentListCreateView.as_view(), name='diarized-segment-list-create'),
    path('diarization/<int:pk>/', DiarizationDetailView.as_view(), name='diarized-detail'),

    path('audio-chunks/', AudioChunkViewSet.as_view({'get': 'list', 'post': 'create'}), name='audio-chunk-list-create'),
    path('audio-chunks/<int:pk>/', AudioChunkViewSet.as_view({'get': 'retrieve'}), name='audio-chunk-detail'),

    path('case_laws/', CaseMatchingListView.as_view(), name='case_laws'),
    path('case_laws/<int:id>/', CaseMatchingDetailView.as_view(), name='case_law'),
]