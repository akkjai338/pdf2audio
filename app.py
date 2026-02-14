from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfReader
from gtts import gTTS
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
AUDIO_FOLDER = "audio"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    file = request.files["pdf_file"]
    language = request.form.get("language")

    if not file:
        return "No file uploaded"

    unique_id = str(uuid.uuid4())
    pdf_path = os.path.join(UPLOAD_FOLDER, unique_id + ".pdf")
    audio_path = os.path.join(AUDIO_FOLDER, unique_id + ".mp3")

    file.save(pdf_path)

    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    if text.strip() == "":
        return "No readable text found"

    tts = gTTS(text=text, lang=language)
    tts.save(audio_path)

    return send_file(audio_path, as_attachment=True)

if __name__ == "__main__":
    app.run()
