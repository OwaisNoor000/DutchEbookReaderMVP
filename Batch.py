#######################################################
# This is the Batch process that preprocesses books
#######################################################

import os
from EPUB_PROCESSOR.EpubProcessor import EpubProcessor
from OCR.OpticalCharacterReader import OpticalCharacterReader
from GCP.SpeechGenerator import generate_and_sync_speech 

def processEPUBs():
    # Get books not yet processed
    unprocessed_books = []
    epub_folder = set()
    preprocessed_folder=set()

    for book in os.listdir("EPUB"):
        epub_folder.add(os.path.splitext(book)[0])

    for book in os.listdir("PREPROCESSED"):
        preprocessed_folder.add(book)

    unprocessed_books = epub_folder.difference(preprocessed_folder)


    for bookName in unprocessed_books:
        # BATCH OPERATION STEP 1: Processing EPUB Pages as images
        print(f"{bookName}: Processing Ebook Pages to IMG")
        epub_processor = EpubProcessor(f"EPUB/{bookName}.epub")
        epub_processor.convert()
        epub_processor.saveAsImg()

        # BATCH OPERATION STEP 2: OCR
        print(f"{bookName}: Reading Ebook Pages and getting word positions")
        ocr = OpticalCharacterReader(f"PREPROCESSED/{bookName}",verbose=True)
        ocr.readImages()
        ocr.readText()
        ocr.getTextMetaData()
        ocr.saveBoxMappingsAsJson()

        # BATCH OPERATION STEP 3: Speech, Time Stamps Generation and Sentence labelling
        print(f"{bookName}: Generating Speech with time stamps and syncing with text")
        generate_and_sync_speech(f"PREPROCESSED/{bookName}")


        with open("batchStatus.txt","w",encoding="UTF-8") as f:
            f.write("Processed")




