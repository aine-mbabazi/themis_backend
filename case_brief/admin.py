from django.contrib import admin
from case_brief.models import CaseBrief

@admin.register(CaseBrief)
class CaseBriefAdmin(admin.ModelAdmin):
    # Define the fields to be displayed in the list view
    list_display = ['transcription', 'case_title', 'case_number', 'judge_name', 'created_at']
    # Define which fields should be editable in the admin form
    fields = [
        'transcription',
        'case_title',
        'case_number',
        'judge_name',
        'accused_name',
        'filtered_transcript',
        'court_type',
        'country',
        'court_location',
        'date',
        'prosecutor_name',
        'defense_counsel_name',
        'charges',
        'plea',
        'verdict',
        'sentence',
        'mitigating_factors',
        'aggravating_factors',
        'legal_principles',
        'precedents_cited'
    ]

    # Enable editing fields directly in the list view (optional)
    list_editable = ['case_title', 'case_number', 'judge_name']


