import json

# read json
with open("transcription.json") as f:
    transcription = json.load(f)

timeStamps = []
items = transcription["results"]["items"]
# convert
sentences = [] 
sentence = ""
for index,item in enumerate(items):
    # print(item)
    word = item["alternatives"][0]["content"]
    if word==".":
        sentence[-1]=word
    else:
        sentence+=" "+ word

    if(item["type"]=="punctuation"):
        # print(sentence)
        sentences.append(sentence)
        sentence = ""

print(sentences)

