from fastapi import FastAPI
import tempfile
import boto3
import os
from botocore.exceptions import ClientError
from audio_features import extract_features
from normalization import normalize_all
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

bucket = os.getenv("AWS_BUCKET_NAME")


def download_file_from_s3(key: str):
    try:

        print("\n========== S3 DEBUG ==========")
        print("RAW KEY:", repr(key))
        print("BUCKET:", bucket)
        print("REGION:", os.getenv("AWS_REGION"))
        print("FULL S3 PATH:", f"s3://{bucket}/{key}")
        print("TRY DOWNLOAD:", bucket, key)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        tmp.close()

        print("TEMP FILE:", tmp.name)

        print("CALLING S3 DOWNLOAD...")

        s3.download_file(bucket, key, tmp.name)

        print("DOWNLOAD SUCCESS")

        file_size = os.path.getsize(tmp.name)
        print("FILE SIZE:", file_size)

        print("========== END DEBUG ==========\n")

        return tmp.name

    except ClientError as e:
        print("\n========== AWS ERROR ==========")
        print(e.response["Error"])
        print("================================\n")
        raise Exception(f"S3 error: {e.response['Error']}")

@app.post("/analyze")
def analyze_audio(payload: dict):
    key = payload.get("key")

    if not key:
        return {"error": "missing key"}

    file_path = download_file_from_s3(key)

    try:
        features = extract_features(file_path)
        normalized = normalize_all(features)

        return {
            "audio_features": normalized
        }

    finally:
        os.remove(file_path)