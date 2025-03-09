import json
from pathlib import Path
from google.cloud import texttospeech_v1beta1 as tts


def go_ssml(current_dir, ssml):
    client = tts.TextToSpeechClient()
    voice = tts.VoiceSelectionParams(
        language_code="nl-NL",
        name="nl-NL-Standard-A",
        ssml_gender=tts.SsmlVoiceGender.FEMALE,
    )

    response = client.synthesize_speech(
        request=tts.SynthesizeSpeechRequest(
            input=tts.SynthesisInput(ssml=ssml),
            voice=voice,
            audio_config=tts.AudioConfig(audio_encoding=tts.AudioEncoding.MP3),
            enable_time_pointing=[
                tts.SynthesizeSpeechRequest.TimepointType.SSML_MARK]
        )
    )

    # cheesy conversion of array of Timepoint proto.Message objects into plain-old data
    marks = [dict(sec=t.time_seconds, name=t.mark_name)
             for t in response.timepoints]

    with open(f"{current_dir}/timeStamps.json",'w') as out:
        json.dump(marks, out)

    with open(f"{current_dir}/speech.mp3",'wb') as out:
        out.write(response.audio_content)

def go_TTS(current_dir):
    with open(f"{current_dir}/markedText.txt",encoding="UTF-8") as f:
        content = f.read()

    go_ssml(current_dir, content)

# go_TTS("PREPROCESSED/Jip&Janneke/PAGE12")