
# from django import forms
# from .models import Transcription
# import boto3
# from botocore.exceptions import NoCredentialsError

# class TranscriptionAdminForm(forms.ModelForm):
#     class Meta:
#         model = Transcription
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super(TranscriptionAdminForm, self).__init__(*args, **kwargs)

     


       
#         try:
#             response = s3_client.list_objects_v2(Bucket='taishibucket')
#             if 'Contents' in response:
#                 choices = [(item['Key'], item['Key']) for item in response['Contents']]
#             else:
#                 choices = []
#         except NoCredentialsError:
#             choices = []
#             print("Credentials not available for S3.")

        
#         self.fields['audio_file'] = forms.ChoiceField(choices=choices, label="Select S3 Audio File")

