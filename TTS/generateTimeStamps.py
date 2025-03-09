"""Getting Started Example for Python 2.7+/3.3+"""
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
import json

def generateTimeStamps(current_dir):
    # Create a client using the credentials and region defined in the [adminuser]
    # section of the AWS credentials file (~/.aws/credentials).
    session = Session(profile_name="default")
    polly = session.client("polly")

    with open(f"{current_dir}/Text.txt",encoding="UTF-8") as f:
        contents = f.read()

    contents = contents.replace("\n"," ").split(" ") # remove new lines
    contents = [i for i in contents if i != ""]
    contents = " ".join(contents)
    contents = contents.replace("&","&amp;")
    contents = contents.replace("'","&apos;")
    contents = contents.replace('"',"&quot;")
    contents = contents.replace("<","&lt;")
    contents = contents.replace(">","&gt;")

    try:
        # Request speech synthesis
        # text = f"<speak><prosody rate='70%'>{contents}</prosody></speak>"
        text = f"{contents}"
        # text = "<speak><prosody rate='80%'>The crazy thing is I wasnt even at her house that day. She is really getting on my nerves</prosody></speak>"
        response = polly.synthesize_speech(
            Text=text, 
            TextType="ssml",
            OutputFormat="json",
            SpeechMarkTypes=["sentence"],
            VoiceId="Laura",
            LanguageCode = "nl-NL",
            Engine="neural"
            )
        
        audio_data = response['AudioStream'].read().decode('utf-8')
        audio_lines = audio_data.strip().split('\n')

        speech_marks = []
        for line in audio_lines:
            try:
                mark = json.loads(line)
                speech_marks.append(mark)
                
            except json.JSONDecodeError as e:
                print(f"JSON decoding error: {e}")

        with open (f"{current_dir}/timeStamps.json","w") as f:
                    json.dump(speech_marks,f)

        # timestamps = []
        # for mark in speech_marks:
        #     if mark['type'] == 'word':
        #         timestamps.append((mark['time'], mark['value']))

        # with open('timestamps.txt', 'w') as txt_file:
        #     for time, word in timestamps:
        #         txt_file.write(f"{time}: {word}\n")
        
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        sys.exit(-1)

