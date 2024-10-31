from django.urls import path

from .views import (
    TranscriptionViewSet,
    DiarizedSegmentListCreateView,
    DiarizationDetailView,
    AudioChunkViewSet,
    CaseMatchingDetailView,
    CaseMatchingListView,
    CaseBriefSegmentListCreateView,
    CaseBriefDetailView,
    download_case_brief_pdf,
)

urlpatterns = [

    path('transcriptions/transcription_status_counts/', TranscriptionViewSet.as_view({'get': 'transcription_status_counts'}), name='transcription-status-counts'),
    path('transcriptions/', TranscriptionViewSet.as_view({'get': 'list', 'post': 'create'}), name='transcription-list'),
    path('transcription/<int:pk>/', TranscriptionViewSet.as_view({'get': 'retrieve'}), name='transcription-detail'),

    # Diarization API paths
    path('diarizations/', DiarizedSegmentListCreateView.as_view(), name='diarized-segment-list-create'),
    path('diarization/<int:pk>/', DiarizationDetailView.as_view(), name='diarized-detail'),

    path('audio-chunks/', AudioChunkViewSet.as_view({'get': 'list', 'post': 'create'}), name='audio-chunk-list-create'),
    path('audio-chunks/<int:pk>/', AudioChunkViewSet.as_view({'get': 'retrieve'}), name='audio-chunk-detail'),

    path('case_laws/', CaseMatchingListView.as_view(), name='case_laws'),
    path('case_laws/<int:id>/', CaseMatchingDetailView.as_view(), name='case_law'),

    path('download_case_brief/transcription/<int:transcription_id>/', download_case_brief_pdf, name='download_case_brief_pdf'),
    path('case_briefs/',  CaseBriefSegmentListCreateView.as_view(), name='case_brief_list'),
    path('case_brief/<int:pk>/', CaseBriefDetailView.as_view(), name='case_brief_detail'),
]