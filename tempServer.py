from flask import Flask, jsonify,send_from_directory,request
import os
from flask_cors import CORS
import cv2
from PIL import Image
from Batch import processEPUBs
import threading

app = Flask(__name__)
CORS(app)

@app.route('/boxes/<book>/<page>')
def serve_json(book,page):
    return send_from_directory(os.getcwd(), f'PREPROCESSED/{book}/PAGE{page}/labelledBoxMappings.json')

@app.route("/stopBoxes.json")
def sendStepBoxes():
    return send_from_directory(os.getcwd(), 'stopBoxes.json')
    
@app.route('/timeStamps/<book>/<page>')
def sendTimeStamps(book,page):
    return send_from_directory(os.getcwd(), f'PREPROCESSED/{book}/PAGE{page}/timeStamps.json')

@app.route('/image/<book>/<page>')
def send_image(book,page):
    return send_from_directory(os.getcwd(), f'PREPROCESSED/{book}/PAGE{page}/Page.jpg')

@app.route("/getAudioChunkUrls")
def sendAudioUrls():
    files_names = [f"localhost:8000/getAudioChunk/{name}" for name in os.listdir("TTS/AUDIO CHUNKS")]
    return jsonify(files_names)

@app.route("/getAudioChunk/<name>")
def getAudioChunk(name):
    file_path = f"TTS/AUDIO CHUNKS/{name}"
    return send_from_directory(os.getcwd(),file_path,mimetype="audio/mp3")

@app.route("/audio/<book>/<page>")
def sendFullAudio(book,page):
     return send_from_directory(os.getcwd(), f'PREPROCESSED/{book}/PAGE{page}/speech.mp3')

@app.route("/general/getEbookNames")
def sendEbookNames():
    ebooks = []

    for book_name in os.listdir("EPUB"):
        ebooks.append(book_name.split(".")[0])

    
    return jsonify({"books":ebooks})


@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the 'file' is part of the request
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file part"}), 400
    
    file = request.files['file']
    
    # Check if the file is an EPUB
    if file and file.filename.endswith('.epub'):
        # Save the file or process it here
        file.save(f"EPUB/{file.filename}")

        with open("batchStatus.txt","w",encoding="UTF-8") as f:
            f.write("Processing")

        thread = threading.Thread(target=processEPUBs)
        thread.start()
        return jsonify({"success": True, "message": "File uploaded successfully!"}), 200
    else:
        return jsonify({"success": False, "message": "Invalid file type. Only EPUB files are allowed."}), 400

@app.route("/getBatchProcessStatus")
def getBatchStatus():
    with open("batchStatus.txt","r",encoding="UTF-8") as f:
        content = f.read()

    return jsonify({"status":content})

if __name__ == '__main__':
    app.run(port=8000,debug=True)