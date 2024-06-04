import requests
from base64 import b64encode,b64decode
import json
import numpy as np
from scipy.io.wavfile import write


url = "http://127.0.0.1:8000/connection"

payload = json.dumps({
  "voice_id":"EN-US",
  "text": "Every morning, Sarah walked her dog, Max, through the old, enchanting forest  her home. One day, thanyou have a noce day",
  "sr": 8000

})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
if response.ok:
    response:dict = json.loads(response.text)
    audio = b64decode(response["audio"])
    print(response["time"])
    with open("text3.wav",'wb') as file:
        file.write(audio)