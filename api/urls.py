from django.urls import path

# from cases.views import transcribed_cases_count
from product_metrics.views import ProductMetricsListView

from .views import (
    TranscriptionViewSet,
    # TranscriptionDetailView,
    DiarizedSegmentListCreateView,
    DiarizationDetailView,
    AudioChunkViewSet
)

urlpatterns = [
    path('transcriptions/transcription_status_counts/', TranscriptionViewSet.as_view({'get': 'transcription_status_counts'}), name='transcription-status-counts'),
    path('transcriptions/', TranscriptionViewSet.as_view({'get': 'list', 'post': 'create'}), name='transcription-list'),
    path('transcription/<int:pk>/', TranscriptionViewSet.as_view({'get': 'retrieve'}), name='transcription-detail'),

    # Metrics API paths
    path('product-metrics/', ProductMetricsListView.as_view(), name='product-metrics-list'),

    # Diarization API paths
    path('diarizations/', DiarizedSegmentListCreateView.as_view(), name='diarized-segment-list-create'),
    path('diarization/<int:pk>/', DiarizationDetailView.as_view(), name='diarized-detail'),

    path('audio-chunks/', AudioChunkViewSet.as_view({'get': 'list', 'post': 'create'}), name='audio-chunk-list-create'),
    path('audio-chunks/<int:pk>/', AudioChunkViewSet.as_view({'get': 'retrieve'}), name='audio-chunk-detail'),
]