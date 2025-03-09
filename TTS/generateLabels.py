import json
import re

def generateLabels(current_dir):
    # read boxMappings
    with open(f"{current_dir}/boxMappings.json","r") as f:
        boxMappings = json.load(f)

    # read timeStamps
    with open(f"{current_dir}/timeStamps.json","r") as f:
        timeStamps = json.load(f)

    # map each word in box Mappings to sentence index in timeStamps
    indexOffset = 0
    line=0
    testFormat = []
    for iteration,stamp in enumerate(timeStamps):

        words = stamp["value"].replace("'"," ").replace("?"," ").replace("’"," ").replace("‘"," ").strip().split(" ")
        words = [i for i in words if i != ""]
        numWordsInSentence = len(words)


        # set the sentence mapping for the words
        sentence = ""
        for i in range(numWordsInSentence):
            boxMappings[i+indexOffset]["class"] = f"line{line}"
            sentence += boxMappings[i+indexOffset]["word"] + " " # compose a sentence
        testFormat.append(sentence)

        line+=1
        indexOffset += numWordsInSentence


    with open(f"{current_dir}/labelledBoxMappings.json","w",encoding="UTF-8") as f:
        json.dump(boxMappings,f)


    # def convertByteToIndex(bite,refText):
    #     encoded_text = refText.encode('utf-8')
    #     substring_bytes = encoded_text[:bite]
    #     char_index = len(substring_bytes.decode('utf-8'))
    #     return char_index

    # with open("OCR/page_contents.txt",encoding="UTF-8") as f:
    #     contents = f.read()

    # contents = contents.replace("\n","") # remove new lines

    # text = contents.replace('"',"&quot;")
    # text = f"<speak><prosody rate='70%'>{contents}</prosody></speak>"
    # for i,stamp in enumerate(timeStamps):
    #     print(i)
    #     start_index = convertByteToIndex(int(stamp["start"]),text)
    #     end_index = convertByteToIndex(int(stamp["end"]),text)
    #     org_sentence = text[start_index:end_index]
    #     actual_sentence = stamp["value"]

    #     print(org_sentence)
    #     print(actual_sentence)
    #     print("\n\n")
