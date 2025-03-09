from GCP.TextMarker import markText
from GCP.GCPTTS import go_ssml,go_TTS
from GCP.MappingLabeller import labelMappings
import os


def generate_and_sync_speech(ebook_path):
    for i,page in enumerate(os.listdir(f"{ebook_path}")):
        print("**********************************************")
        print("doing page",i)
        try:
            markText(f"{ebook_path}/{page}")
        except Exception as e:
            print("skipping text marks for page",i+1)
            print(e)

        try:
            go_TTS(f"{ebook_path}/{page}")
        except Exception as e:
            print("skipping speech and time stamps for page",i+1)
            print(e)

        try:
            labelMappings(f"{ebook_path}/{page}")
        except Exception as e:
            print("skipping label mappings for page",i+1)
            print(e)
        print("**********************************************")

        
