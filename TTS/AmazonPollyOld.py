from generateSpeech import generateSpeech
from generateTimeStamps import generateTimeStamps
from generateLabels import generateLabels
import os

ebook_path = "PREPROCESSED/Jip&Janneke"

# for i,page in enumerate(os.listdir(f"{ebook_path}")):
#     print("doing page",i)
#     generateSpeech(f"{ebook_path}/{page}")
#     generateTimeStamps(f"{ebook_path}/{page}")

#     try:
#         generateLabels(f"{ebook_path}/{page}")
#     except Exception as e:
#         print("skipping time stamps for page",i+1)
#         print(e)


# generateSpeech("PREPROCESSED/Jip&Janneke/PAGE6")
generateTimeStamps("PREPROCESSED/Jip&Janneke/PAGE6")
# generateLabels("PREPROCESSED/Jip&Janneke/PAGE6")