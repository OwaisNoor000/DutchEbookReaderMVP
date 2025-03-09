import pytesseract
import cv2
import os
import json

class OpticalCharacterReader():
    def __init__(self,img_dir,verbose=False):
        if(verbose):
            print("OCR Initialized")
        self.img_dir = img_dir
        self.tesseractDir = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        self.pageContents = []
        self.wordsBoxes = []
        self.images = []
        self.stopBoxes = []
        self.verbose = verbose
        pytesseract.pytesseract.tesseract_cmd = self.tesseractDir
    def readImages(self):
        if(self.verbose):
            print("Reading Images")
        localImages = []

        for name in os.listdir(self.img_dir):
            image = cv2.imread(f"{self.img_dir}/{name}/Page.jpg")
            localImages.append(image)
        self.images = localImages

    def readText(self):
        if(self.verbose):
            print("Reading Text")
        localPageContents = []
        for image in self.images:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray)
            print(text)
            localPageContents.append(text)
        
        self.pageContents = localPageContents
        
        for i,name in enumerate(os.listdir(self.img_dir)):
            with open(f"{self.img_dir}/{name}/Text.txt","w",encoding="UTF-8") as f:
                f.write(localPageContents[i])

    
    def getTextMetaData(self):
        if(self.verbose):
            print("Getting Text Metadata")
        localWordBoxes = []
        for image in self.images: # for every page
            data = pytesseract.image_to_data(image,output_type=pytesseract.Output.DICT)
            pageMetadata = []
            for i in range(len(data["text"])): # for every word in the image
                if data["text"][i].strip():  # Ignore empty words
                    x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
                    metadata = {"word":data["text"][i],"position":(x,y,w,h)}  
                    pageMetadata.append(metadata)
            localWordBoxes.append(pageMetadata)
        self.wordsBoxes = localWordBoxes

    def saveBoxMappingsAsJson(self):
        if(self.verbose):
            print("Saving Box Mappings as JSON")
        
        for i,name in enumerate(os.listdir(self.img_dir)):
            with open(f"{self.img_dir}/{name}/boxMappings.json","w",encoding="UTF-8") as f:
                json.dump(self.wordsBoxes[i],f)
        # with open("OCR/boxMappings.json","w") as f:
        #     json.dump(self.wordsBoxes,f)

    def getSentenceEndingBoxes(self,):
        if(self.verbose):
            print("Getting Sentence Ending Boxes")
        localStopBoxes = []
        for contents in self.wordsBoxes:
            stop_values = []
            for wordMetaData in contents:
                if "." in wordMetaData["word"]:
                    stop_values.append(wordMetaData)
            localStopBoxes.append(stop_values)
        self.stopBoxes = localStopBoxes

        with open("stopBoxes.json","w") as file:
            json.dump(localStopBoxes,file)

    def labelBoxIds(self,):
        i = 0
        localWordBoxes = self.wordsBoxes.copy()
        for content in localWordBoxes:
            for word in content:
                word["id"] = f"line{i}"
                if "." in word["word"]:
                    i+=1
        
        with open("OCR/labelledBoxMappings.json","w") as file:
            json.dump(localWordBoxes,file)



 
# ocr = OpticalCharacterReader("PREPROCESSED/Jip&Janneke",verbose=True)
# ocr.readImages()
# ocr.readText()
# ocr.getTextMetaData()
# ocr.saveBoxMappingsAsJson()

# ocr.getSentenceEndingBoxes()
# ocr.labelBoxIds()