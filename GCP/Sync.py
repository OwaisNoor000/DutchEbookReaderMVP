import json,re

current_dir = "PREPROCESSED/Jip&Janneke/PAGE16"

with open(f"{current_dir}/labelledBoxMappings.json") as f:
    boxMappings = json.load(f)

with open(f"{current_dir}/markedText.txt",encoding="UTF-8") as f:
    timeStamps = f.read()

OCR_sentences = []
line = "line0"
sentence = ""
for mapping in boxMappings:
    if mapping["class"]!=line:
        OCR_sentences.append(sentence.replace("\n",""))
        sentence=""
        line=mapping["class"]

    sentence += mapping["word"] + " "
OCR_sentences.append(sentence)

stampedSentences = []
state = ""
sentence = ""

for stamp in timeStamps:
    if stamp==">":
        state="begin"
        continue
    if stamp == "<":
        state="end"

    if state=="begin":
        sentence+=stamp

    if state=="end":
        stampedSentences.append(sentence)
        sentence=""
        state=""


stampedSentences = [i.replace("\n","") for i in stampedSentences if i !=""]

with open("GCP/Sync.txt","w",encoding="UTF-8") as f:
    for i,ocr_sentence in enumerate(OCR_sentences):
        f.write(f"OCR {ocr_sentence}")
        f.write("\n")
        f.write(f"GCP {stampedSentences[i]}")
        f.write("\n")
        f.write("\n")



    



