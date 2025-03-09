import os
import threading
from EPUB_PROCESSOR.EpubProcessor import EpubProcessor
from OCR.OpticalCharacterReader import OpticalCharacterReader
from GCP.SpeechGenerator import generate_and_sync_speech


# Function to process a single book
def process_book(bookName):
    try:
        # BATCH OPERATION STEP 1: Processing EPUB Pages as images
        print(f"{bookName}: Processing Ebook Pages to IMG")
        epub_processor = EpubProcessor(f"EPUB/{bookName}.epub")
        epub_processor.convert()
        epub_processor.saveAsImg()

        # List of images to be processed by OCR
        image_files = os.listdir(f"PREPROCESSED/{bookName}")
        total_images = len(image_files)

        # BATCH OPERATION STEP 2: OCR
        print(f"{bookName}: Reading Ebook Pages and getting word positions")
        ocr = OpticalCharacterReader(f"PREPROCESSED/{bookName}", verbose=True)
        for idx, image_file in enumerate(image_files):
            print(f"{bookName}: OCR Processing Image {idx+1}/{total_images} ({image_file})")
            ocr.readImages(image_file)
            ocr.readText(image_file)
            ocr.getTextMetaData()
            ocr.saveBoxMappingsAsJson(image_file)

        # BATCH OPERATION STEP 3: Speech, Time Stamps Generation and Sentence labelling
        print(f"{bookName}: Generating Speech with time stamps and syncing with text")
        generate_and_sync_speech(f"PREPROCESSED/{bookName}")

    except Exception as e:
        print(f"Error processing {bookName}: {str(e)}")