# converts time stamps to labelledBoxMappings

import json
import re

def labelMappings(current_dir):
    # read boxMappings
    with open(f"{current_dir}/boxMappings.json","r") as f:
        boxMappings = json.load(f)

    # read timeStamps
    # with open(f"{current_dir}/timeStamps.json","r") as f:
    #     timeStamps = json.load(f)

    def removeUnicode(sentence):
        return re.sub(r'\\u[0-9a-fA-F]+', '', sentence)

    # map each word in box Mappings to sentence index in timeStamps
    sentenceNo = 0
    for mapping in boxMappings:
        mapping["class"] = f"line{sentenceNo}"
        if "." in mapping["word"]:
            sentenceNo+=1
        
    with open(f"{current_dir}/labelledBoxMappings.json","w",encoding="UTF-8") as f:
        json.dump(boxMappings,f)

# labelMappings("PREPROCESSED/Jip&Janneke/PAGE12")