"""Getting Started Example for Python 2.7+/3.3+"""
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir

# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).


def generateSpeech(ebook_path):
    session = Session(profile_name="default")
    polly = session.client("polly")

    with open(f"{ebook_path}/Text.txt",encoding="UTF-8") as f:
        contents = f.read()

    contents = contents.replace("\n","") # remove new lines
    contents = contents.replace("&","&amp;")
    contents = contents.replace("'","&apos;")
    contents = contents.replace('"',"&quot;")
    contents = contents.replace("<","&lt;")
    contents = contents.replace(">","&gt;")
    print(contents)

    try:
        # Request speech synthesis
        # text = contents.replace('"',"&quot;")
        # text = f"<speak><prosody rate='70%'>{contents}</prosody></speak>"
        text = f"{contents}"
        response = polly.synthesize_speech(
            Text=text, 
            TextType="ssml",
            OutputFormat="mp3",
            VoiceId="Laura",
            LanguageCode = "nl-NL",
            # LanguageCode = "en-GB",
            Engine="neural"
            )
        
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        sys.exit(-1)

    # Access the audio stream from the response
    if "AudioStream" in response:
        # Note: Closing the stream is important because the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
            with closing(response["AudioStream"]) as stream:
                output = f"{ebook_path}/speech.mp3"

                try:
                    # Open a file for writing the output as a binary stream
                        with open(output, "wb") as file:
                            file.write(stream.read())
                except IOError as error:
                    # Could not write to file, exit gracefully
                    print(error)
                    sys.exit(-1)

    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        sys.exit(-1)

  