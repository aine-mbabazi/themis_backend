from django.contrib import admin
from .models import Case_matching

# Register your models here.

@admin.register(Case_matching)
class Case_matchingAdmin(admin.ModelAdmin):
    list_display = ['transcription', 'date_created']
    readonly_fields = ['case']
