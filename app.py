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
    language = request.form.get("language")
    text = request.form.get("text")
    file = request.files.get("pdf_file")

    extracted_text = ""

    # If user entered text
    if text and text.strip() != "":
        extracted_text = text

    # If user uploaded PDF
    elif file:
        unique_id_pdf = str(uuid.uuid4())
        pdf_path = os.path.join(UPLOAD_FOLDER, unique_id_pdf + ".pdf")
        file.save(pdf_path)

        reader = PdfReader(pdf_path)
        for page in reader.pages:
            if page.extract_text():
                extracted_text += page.extract_text()

    else:
        return "Please enter text or upload a PDF"

    if extracted_text.strip() == "":
        return "No readable text found"

    # Limit text length
    extracted_text = extracted_text[:5000]

    unique_id_audio = str(uuid.uuid4())
    audio_path = os.path.join(AUDIO_FOLDER, unique_id_audio + ".mp3")

    tts = gTTS(text=extracted_text, lang=language)
    tts.save(audio_path)

    return send_file(audio_path, as_attachment=True)

if __name__ == "__main__":
    app.run()
