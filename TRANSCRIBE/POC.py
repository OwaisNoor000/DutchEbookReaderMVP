import time
import boto3
import requests
import json
import random
import string

def generate_str(length=6):
    # Use only letters (both uppercase and lowercase)
    return ''.join(random.choices(string.ascii_letters, k=length))

def transcribe_file(job_name, file_uri, transcribe_client):
    transcribe_client.start_transcription_job(
        TranscriptionJobName = job_name,
        Media = {
            'MediaFileUri': file_uri
        },
        MediaFormat = 'flac',
        LanguageCode = 'nl-NL'
    )

    max_tries = 60
    while max_tries > 0:
        max_tries -= 1
        job = transcribe_client.get_transcription_job(TranscriptionJobName = job_name)
        job_status = job['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            print(f"Job {job_name} is {job_status}.")
            if job_status == 'COMPLETED':
                output_uri = job['TranscriptionJob']['Transcript']['TranscriptFileUri']
                response = requests.get(output_uri)
                if response.status_code == 200:
                    json_data = response.json()
                    with open("transcription.json","w",encoding="UTF-8") as f:
                        json.dump(json_data,f)

            break
        else:
            print(f"Waiting for {job_name}. Current status is {job_status}.")
        time.sleep(10)


def main():
    transcribe_client = boto3.client('transcribe', region_name = 'eu-north-1')
    file_uri = 's3://noorway/speech.mp3'
    transcribe_file(f'{generate_str()}', file_uri, transcribe_client)


if __name__ == '__main__':
    main()