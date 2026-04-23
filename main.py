from fastapi import FastAPI, UploadFile, File
import tempfile
import os

from audio_features import extract_features
from normalization import normalize_all

app = FastAPI()


@app.post("/analyze")
async def analyze_audio(audio: UploadFile = File(...)):

    if not audio:
        return {"error": "missing audio file"}

    # יצירת קובץ זמני
    suffix = ".webm"  # כי זה מה שהקליינט שולח
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)

    try:
        # קריאת הקובץ מה-Node
        content = await audio.read()
        tmp.write(content)
        tmp.close()

        file_path = tmp.name

        # ניתוח אודיו
        features = extract_features(file_path)
        normalized = normalize_all(features)

        return {
            "audio_features": normalized
        }

    finally:
        # ניקוי קובץ זמני
        try:
            os.remove(tmp.name)
        except:
            pass