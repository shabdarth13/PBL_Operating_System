import os
import urllib.request
import zipfile
import sys
from pathlib import Path

def download_vosk_model(model_url: str = None, extract_to: str = "models"):

    
    if model_url is None:
        model_url = "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip"
    
    model_name = os.path.basename(model_url).replace('.zip', '')
    model_zip_path = os.path.join(extract_to, os.path.basename(model_url))
    model_extract_path = os.path.join(extract_to, model_name)
    os.makedirs(extract_to, exist_ok=True)
    if os.path.exists(model_extract_path):
        print(f"Model already exists at {model_extract_path}")
        return model_extract_path
    
    print(f"Downloading Vosk model from {model_url}...")
    
    try:
        urllib.request.urlretrieve(model_url, model_zip_path)
        print("Download completed!")
        print("Extracting model...")
        with zipfile.ZipFile(model_zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        os.remove(model_zip_path)
        
        print(f"Model extracted to {model_extract_path}")
        return model_extract_path
        
    except Exception as e:
        print(f"Error downloading model: {e}")
       
        if os.path.exists(model_zip_path):
            os.remove(model_zip_path)
        return None

if __name__ == "__main__":
    model_path = download_vosk_model()
    if model_path:
        print(f"Vosk model ready at: {model_path}")
    else:
        print("Failed to download Vosk model")
        sys.exit(1)