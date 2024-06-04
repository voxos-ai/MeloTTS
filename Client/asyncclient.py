import aiohttp
import asyncio
from base64 import b64decode
import json
import numpy as np
from scipy.io.wavfile import write

async def fetch_audio():
    url = "http://127.0.0.1:8000/connection"
    payload = {
        "voice_id": "EN-US",
        "text": "Every morning, Sarah walked her dog, Max, through the old, enchanting forest near her home. One day, thanyou have a nice day",
        "sr": 8000,
        "sdp_ratio" : 0.2,
        "noise_scale" : 0.6,
        "noise_scale_w" :  0.8,
        "speed" : 1.0
    }
    headers = {
        'Content-Type': 'application/json'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 200:
                response_data = await response.json()
                audio = b64decode(response_data["audio"])
                print(response_data["time"])
                with open("text7.wav",'wb') as file:
                    file.write(audio)
            else:
                error_message = await response.text()
                print(f"Error {response.status}: {error_message}")
                print(f"Response headers: {response.headers}")

# Run the asynchronous function
loop = asyncio.get_event_loop()
loop.run_until_complete(fetch_audio())
