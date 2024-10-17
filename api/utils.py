import requests
import time
import json
import assemblyai as aai
from io import BytesIO
import logging
from django.conf import settings
import re
# Set the AssemblyAI API key
aai.settings.api_key = settings.AAI_KEY


# def transcribe_audio_with_retry(audio_file_path, retries=5, delay=2):
#     """Transcribes audio and retries with exponential backoff in case of failure."""
#     transcriber = aai.Transcriber()
#     for attempt in range(retries):
#         try:
#             with open(audio_file_path, 'rb') as audio_file:
#                 print(f"Transcribing file: {audio_file_path} (Attempt {attempt+1})")  # Debugging line
#                 transcript = transcriber.transcribe(audio_file)

#             if transcript.status == aai.TranscriptStatus.error:
#                 print(f"Transcription Error: {transcript.error}")  # Debugging line
#                 raise ValueError(f"Transcription Error: {transcript.error}")

#             if transcript.status == aai.TranscriptStatus.completed:
#                 print(f"Transcription completed for file: {audio_file_path}")  # Debugging line
#                 print(f"Transcribed text: {transcript.text}")  # Debugging line
#                 return transcript.text

#             print(f"Unexpected transcription status: {transcript.status}")  # Debugging line
#             raise ValueError(f"Unexpected transcription status: {transcript.status}")

#         except requests.exceptions.Timeout as e:
#             print(f"Timeout during transcription: {e}. Retrying in {delay ** attempt} seconds.")  # Debugging line
#             time.sleep(delay ** attempt)
#         except Exception as e:
#             print(f"Error transcribing file {audio_file_path}: {e}")  # Debugging line
#             return None
#     print(f"All attempts failed for file: {audio_file_path}")
#     return None






import openai

# Set your OpenAI API key
openai.api_key = settings.OPENAI_API_KEY

def transcribe_audio_with_retry(audio_file_path, retries=5, delay=2):
    """Transcribes audio using OpenAI Whisper API with retries and exponential backoff."""
    
    for attempt in range(retries):
        try:
            with open(audio_file_path, 'rb') as audio_file:
                print(f"Transcribing file: {audio_file_path} (Attempt {attempt+1})")  # Debugging line

                # Use OpenAI's Whisper model for transcription
                transcription = openai.Audio.transcribe(
                    model="whisper-1", 
                    file=audio_file,
                    language="en"
                )

                if 'error' in transcription:
                    print(f"Transcription Error: {transcription['error']}")  # Debugging line
                    raise ValueError(f"Transcription Error: {transcription['error']}")

                print(f"Transcription completed for file: {audio_file_path}")  # Debugging line
                return transcription['text']

        except Exception as e:
            print(f"Error transcribing file {audio_file_path}: {e}")  # Debugging line
            if attempt < retries - 1:
                print(f"Retrying in {delay ** attempt} seconds.")  # Debugging line
                time.sleep(delay ** attempt)
            else:
                print(f"All attempts failed for file: {audio_file_path}")
                return None




from pyannote.audio import Pipeline

# Initialize the diarization pipeline (use your Hugging Face access token if needed)
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1",  use_auth_token=settings.HF_AUTH_TOKEN)

def diarize_audio_with_retry(audio_file_path, retries=5, delay=2):
    """Performs diarization and transcription on the given audio file with retry logic using pyannote.audio and OpenAI."""
    
    for attempt in range(retries):
        try:
            print(f"Starting diarization for file: {audio_file_path} (Attempt {attempt+1})")
            
            # Step 1: Run diarization with pyannote
            diarization_result = pipeline(audio_file_path)
            
            # Step 2: Run transcription with Whisper API (OpenAI)
            with open(audio_file_path, 'rb') as audio_file:
                transcription_response = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file,
                    language="en"
                )
                transcription_text = transcription_response.get('text', '')

            if not transcription_text:
                raise ValueError(f"No transcription found for {audio_file_path}")
            
            print(f"Transcription and diarization completed for file: {audio_file_path}")

            # Step 3: Align the transcription with speaker segments (diarization)
            speaker_texts = align_diarization_with_transcription(diarization_result, transcription_text)

            return speaker_texts  # Return the aligned speaker text

        except Exception as e:
            print(f"Error during diarization or transcription of file {audio_file_path}: {e}")
            if attempt < retries - 1:
                print(f"Retrying in {delay ** attempt} seconds.")
                time.sleep(delay ** attempt)
            else:
                print(f"All attempts failed for diarization of file: {audio_file_path}")
                return None


def align_diarization_with_transcription(diarization_result, transcription_text):
    """Aligns transcription text with speaker segments based on diarization results."""
    words = transcription_text.split()  # Split the transcription into words
    word_index = 0
    speaker_texts = []
    current_speaker = None
    current_speaker_text = []

    for turn, _, speaker in diarization_result.itertracks(yield_label=True):
        # Estimate the number of words for this segment based on its length
        segment_duration = turn.end - turn.start
        segment_word_count = int(len(words) * (segment_duration / diarization_result.get_timeline().extent().duration))

        # Get the words for this segment and move the index forward
        segment_words = words[word_index:word_index + segment_word_count]
        segment_text = " ".join(segment_words)

        # If the speaker is the same as the previous one, concatenate the text
        if speaker == current_speaker:
            current_speaker_text.append(segment_text)
        else:
            # If we switched speakers, store the current speaker's text and start a new block
            if current_speaker is not None:
                speaker_texts.append({
                    "speaker": current_speaker,
                    "text": " ".join(current_speaker_text)
                })

            # Start a new speaker block
            current_speaker = speaker
            current_speaker_text = [segment_text]

        word_index += segment_word_count

    # Append the last speaker's text after loop ends
    if current_speaker is not None:
        speaker_texts.append({
            "speaker": current_speaker,
            "text": " ".join(current_speaker_text)
        })

    return speaker_texts


def format_diarization(diarization_data):
    """Formats diarization data to include simplified speaker labels and their spoken text."""
    formatted_data = []
    for index, utterance in enumerate(diarization_data):
        speaker = f"Speaker {index + 1}"  # Simplify speaker label to Speaker 1, Speaker 2, etc.
        text = utterance['text']  # Get the spoken text
        formatted_data.append(f"{speaker}: {text}\n\n")  # Add extra space for readability

    return ''.join(formatted_data)  # Join the formatted text into a single string











# def diarize_audio_with_retry(audio_file_path, retries=5, delay=2):
#     """Performs diarization on the given audio file with retry logic."""
#     transcriber = aai.Transcriber()
#     config = aai.TranscriptionConfig(speaker_labels=True)  # Enable speaker labeling (diarization)

#     for attempt in range(retries):
#         try:
#             with open(audio_file_path, 'rb') as audio_file:
#                 print(f"Starting diarization for file: {audio_file_path} (Attempt {attempt+1})")
#                 transcript = transcriber.transcribe(audio_file, config=config)

#             if transcript.status == aai.TranscriptStatus.error:
#                 print(f"Diarization Error: {transcript.error}")
#                 raise ValueError(f"Diarization Error: {transcript.error}")

#             if transcript.status == aai.TranscriptStatus.completed:
#                 print(f"Diarization completed for file: {audio_file_path}")
#                 return transcript.utterances  # Return utterances for chunk

#             print(f"Unexpected diarization status: {transcript.status}")
#             raise ValueError(f"Unexpected diarization status: {transcript.status}")

#         except requests.exceptions.Timeout as e:
#             print(f"Timeout during diarization: {e}. Retrying in {delay ** attempt} seconds.")
#             time.sleep(delay ** attempt)
#         except Exception as e:
#             print(f"Error during diarization of file {audio_file_path}: {e}")
#             return None

#     print(f"All attempts failed for diarization of file: {audio_file_path}")
#     return None


# def format_diarization(diarization_data):
#     """Formats diarization data to include bold speaker tags and space between dialogues."""
#     formatted_data = []
#     for utterance in diarization_data:
#         speaker = f"**Speaker {utterance['speaker']}**"  # Get the speaker's tag
#         text = utterance['text']  # Get the spoken text
#         formatted_data.append(f"{speaker}: {text}\n")  # Format the speaker and text

#     return ''.join(formatted_data)  # Join the formatted text into a single string



from fpdf import FPDF
import re

def save_as_pdf(case_brief, filename, image_path=None):
    """Saves the given case brief as a PDF file."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    if image_path:
        pdf.image(image_path, x=(pdf.w - 40) / 2, y=10, w=40, h=40)
    
    pdf.ln(50)

    # Split the brief into sections
    sections = case_brief.split('RULING ON SENTENCING')
    
    # Handle cases where 'RULING ON SENTENCING' is not found
    if len(sections) == 1:
        header = ''
        ruling = case_brief
    else:
        header = sections[0].strip()
        ruling = 'RULING ON SENTENCING' + sections[1].strip()

    # Add the header (everything before "RULING ON SENTENCING")
    pdf.set_font("Times", style='B', size=13)
    for line in header.split('\n'):
        if line.strip():
            pdf.cell(0, 10, line.strip(), align='C', ln=True)
        else:
            pdf.ln(5)

    pdf.ln(10)

    # Add "RULING ON SENTENCING" centered and bold
    if len(sections) > 1:
        pdf.cell(0, 10, 'RULING ON SENTENCING', align='C', ln=True)
        pdf.ln(10)

    # Add the content (everything after "RULING ON SENTENCING")
    pdf.set_font("Times", size=12)
    content = ruling.split('DATED, SIGNED AND DELIVERED')[0].strip()
    
    # Handle bold text
    def add_text_with_bold(pdf, text):
        parts = re.split(r'(\[b\].*?\[/b\])', text)
        for part in parts:
            if part.startswith('[b]') and part.endswith('[/b]'):
                pdf.set_font("Times", style='B', size=12)
                pdf.multi_cell(0, 10, part[3:-4], align='J')
            else:
                pdf.set_font("Times", size=12)
                pdf.multi_cell(0, 10, part, align='J')

    add_text_with_bold(pdf, content)

    pdf.ln(10)

    # Add the footer (everything after the content)
    footer_parts = ruling.split('DATED, SIGNED AND DELIVERED')
    if len(footer_parts) > 1:
        pdf.set_font("Times", style='B', size=13)
        footer = 'DATED, SIGNED AND DELIVERED' + footer_parts[1]
        for line in footer.split('\n'):
            if line.strip():
                pdf.cell(0, 10, line.strip(), align='C', ln=True)
            else:
                pdf.ln(5)

    pdf.output(filename)



