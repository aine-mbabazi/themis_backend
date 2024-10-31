# case_brief/admin.py
from django.contrib import admin
from .models import CaseBrief

class CaseBriefAdmin(admin.ModelAdmin):
    list_display = ['transcription','formatted_Casebrief', 'created_at']
    readonly_fields = ['generated_caseBrief','formatted_Casebrief']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Generate the case brief when a transcription is selected and the object is saved
        obj.generate_case_brief()

admin.site.register(CaseBrief, CaseBriefAdmin)
