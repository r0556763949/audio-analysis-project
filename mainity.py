from fastapi import FastAPI
import tempfile
import requests
import os
from pydantic import BaseModel
from typing import Optional
from audio_features import extract_features
from normalization import normalize_all

app = FastAPI()


# ---------------------------
# קבלת קובץ (מקומי או URL)
# ---------------------------
def resolve_file(file_path=None, file_url=None):

    # מצב 1: קובץ מקומי
    if file_path:
        return file_path

    # מצב 2: URL (כולל S3 בעתיד)
    if file_url:
        response = requests.get(file_url)

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        tmp.write(response.content)
        tmp.close()

        return tmp.name

    raise ValueError("No file_path or file_url provided")

class AudioRequest(BaseModel):
    audioKey: Optional[str] = None
    file_url: Optional[str] = None

# ---------------------------
# API
# ---------------------------
@app.post("/analyze")
def analyze(payload: AudioRequest):

    file_path = payload.audioKey
    file_url = payload.file_url
    print("@@@@audioKey:", payload.audioKey)
    print("file_url:", payload.file_url)
    # 1. קבלת קובץ
    audio_file = resolve_file(file_path, file_url)

    # 2. חילוץ פיצ'רים
    features = extract_features(audio_file)

    # 3. נרמול
    normalized = normalize_all(features)

    return {
         "audio_features": normalized
    }