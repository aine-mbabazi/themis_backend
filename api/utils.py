import time
from django.conf import settings
# Set the AssemblyAI API key
# aai.settings.api_key = settings.AAI_KEY

import openai

# Set your OpenAI API key
openai.api_key = settings.OPENAI_API_KEY

def transcribe_audio_with_retry(audio_file_path, retries=5, delay=2):
    """Transcribes audio using OpenAI Whisper API with retries and exponential backoff."""
    
    for attempt in range(retries):
        try:
            with open(audio_file_path, 'rb') as audio_file:
                print(f"Transcribing file: {audio_file_path} (Attempt {attempt+1})") 

                # Use OpenAI's Whisper model for transcription
                transcription = openai.Audio.transcribe(
                    model="whisper-1", 
                    file=audio_file,
                    language="en"
                )

                if 'error' in transcription:
                    print(f"Transcription Error: {transcription['error']}") 
                    raise ValueError(f"Transcription Error: {transcription['error']}")

                print(f"Transcription completed for file: {audio_file_path}") 
                return transcription['text']

        except Exception as e:
            print(f"Error transcribing file {audio_file_path}: {e}") 
            if attempt < retries - 1:
                print(f"Retrying in {delay ** attempt} seconds.") 
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
            
            diarization_result = pipeline(audio_file_path)
            
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

            speaker_texts = align_diarization_with_transcription(diarization_result, transcription_text)

            return speaker_texts 

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
    words = transcription_text.split() 
    word_index = 0
    speaker_texts = []
    current_speaker = None
    current_speaker_text = []

    for turn, _, speaker in diarization_result.itertracks(yield_label=True):

        # Estimating the number of words for this segment based on its length
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
        speaker = f"Speaker {index + 1}" 
        text = utterance['text'] 
        formatted_data.append(f"{speaker}: {text}\n\n") 

    return ''.join(formatted_data)