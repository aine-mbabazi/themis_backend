# Create your views here.
# views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Case

@api_view(['GET'])
def transcribed_cases_count(request):
    transcribed_cases_count = Case.objects.filter(is_transcribed=True).count()
    return Response({
        'success': True,
        'transcribed_cases': transcribed_cases_count
    })
