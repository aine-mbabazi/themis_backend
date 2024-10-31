from django.db import models
from transcription.models import Transcription
from api.utils import extract_case_info_from_transcription, format_case_brief,save_as_pdf
from django.urls import reverse
import os


# Define the CaseBrief model
class CaseBrief(models.Model):
    transcription = models.OneToOneField(Transcription, on_delete=models.CASCADE)
    generated_caseBrief = models.TextField(blank=True, null=True)
    formatted_Casebrief = models.TextField(blank=True, null=True)
    pdf_file_path = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Case Brief for {self.transcription.case_name or 'Unknown Case'}"


    def generate_case_brief(self):
        # Ensure the transcription is available and has the necessary text
        if self.transcription and self.transcription.transcription_text:
            # Extract case information
            case_info = extract_case_info_from_transcription(self.transcription.transcription_text)
            
            # Format the extracted information into a case brief
            self.generated_caseBrief = format_case_brief(case_info)
            
            # Define the path to save the PDF file
            pdf_path = f'media/casebrief_pdf_files/case_brief_{self.id}.pdf'
            
            # Generate and save the PDF
            save_as_pdf(self.generated_caseBrief, pdf_path, image_path='images/themis_logo.png')
            
            # Update the PDF file path in the model
            self.pdf_file_path = pdf_path
            self.save()