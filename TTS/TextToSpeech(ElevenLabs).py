from elevenlabs import ElevenLabs
from elevenlabs import VoiceSettings
import base64
import subprocess
import json 

class TextToSpeech:
    def __init__(self,speed=0.5,file_name="page.mp3"):
        self.start_stamps = []
        self.end_stamps = []
        self.speed = speed
        self.client = ElevenLabs(api_key="sk_382bd2b2ab0b9be7f729a387f9528a3e97d4ad0d70ca7108",)
        self.file_name = file_name
        self.response = None

    def _preprocessText(self,text):
        text = text.replace("\n","")
        text = text.replace("‘",'"')
        text = text.replace("’",'"')
        return text
    
    def convertToSpeech(self,text):
        text = self._preprocessText(text)

        response = self.client.text_to_speech.convert_with_timestamps(
        voice_id="T6sdx9oLQ9xfxeKIi6AM",
        text=text,
        output_format="mp3_22050_32",
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
            speed=self.speed,
            ),
        )
        self.response = response

    def saveAudio(self):        
        # save the audio
        audio_data = base64.b64decode(self.response.audio_base_64)
        audio_path = f"TTS/AUDIO/{self.file_name}"  # Change to .wav if needed
        with open(audio_path, "wb") as audio_file:
            audio_file.write(audio_data)



    def chunkAudioBySentence(self):
        # chunk audio
        alignment = self.response.alignment
        characters = alignment.characters
        start_times = alignment.character_start_times_seconds
        end_times = alignment.character_end_times_seconds

        # get sentence ending indexes
        stop_indexes=[]

        for i,char in enumerate(characters):
            if "." in char:
                stop_indexes.append(i)

        sentence_end_times = [end_times[i] for i in stop_indexes]

        with open("sentenceEndTimes.json","w") as f:
            json.dump(sentence_end_times,f)


        # start_time = 0
        # mp3_file = f"TTS/AUDIO/{self.file_name}"
        # for i, end_time in enumerate(sentence_end_times):
        #     output_file = f"TTS/AUDIO CHUNKS/chunk_{i}.mp3"
        #     duration = end_time - start_time
        #     command = [
        #         "ffmpeg", "-i", mp3_file, "-ss", str(start_time),
        #         "-t", str(duration), "-c", "copy", output_file, "-y"
        #     ]
        #     subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        #     start_time = end_time  # Move to next chunk
        #     print(f"Saved: {output_file}")



tts = TextToSpeech(speed=0.7,file_name="zeroptseven.mp3")
text = 'Een brief aan Sinterklaas\n\n‘Ik heb Sinterklaas gezien,’ zegt Jip.\n\n‘Waar dan?’ vraagt Janneke.\n\n‘In de krant,’ zegt Jip.\n\n‘O, in de krant,’ zegt Janneke. ‘Ik heb hem ook in de\nkrant gezien. Maar hij is er nog niet.’\n\n‘Ja, maar,’ zegt Jip, ‘ik wil zo graag mijn schoentje\nzetten.’\n\n‘He ja,’ zegt Janneke. ‘Hier bij jou thuis Jip. Mijn\nmoeder zegt dat het nog te vroeg is.’\n\nZe halen allebei een schoen en zetten die naast de\nkachel.\n\n‘Je ziet het haast niet, hé?’ zegt Jip.\n\n‘Nee,’ zegt Janneke. ‘Sinterklaas zal er geen erg in\nhebben. Zullen we nog meer schoenen ernaast zetten?’\n\n‘Hé ja,’ zegt Jip. ‘Haal jij ook maar meer, bij je thuis.’\n\nDan hebben ze eindelijk een heleboel schoenen staan.\n\n‘En nu zingen,’ zegt Janneke. ‘Heel hard.’\n\nZe zingen ontzettend hard.\n\nMaar dan komt Jips moeder en zegt: ‘Wat is dat nu?\nSinterklaas is er nog lang niet. Jullie zijn veel te vroeg.\nMaar je mag wel een brief aan Sinterklaas schrijven. Dat\nkan. Doe dat maar.’\n\nZe schrijven een mooie brief. Jip tekent een vrachtauto.\nEn Janneke tekent een fornuisje. Want dat willen ze het\nliefste hebben.\n\n'
# text = 'Een brief aan Sinterklaas\n\n‘Ik heb Sinterklaas gezien,’ zegt Jip.\n\n‘Waar dan?’ vraagt Janneke.\n\n‘In de krant,’ zegt Jip.'
tts.convertToSpeech(text)
tts.saveAudio()
tts.chunkAudioBySentence()