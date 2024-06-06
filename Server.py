from melo.api import TTS
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from base64 import b64encode, b64decode
from contextlib import asynccontextmanager
import torch
import torchaudio.transforms as T
from typing import Optional
import time
from utils import write_bytesIO

TTS_Server = None
speaker_ids = None
@asynccontextmanager
async def lifespan(app: FastAPI):
    global TTS_Server
    global speaker_ids
    # Load the ML model
    TTS_Server = TTS('EN',device='cuda:1')
    speaker_ids = TTS_Server.hps.data.spk2id
    yield
    # Clean up the ML models and release the resources
    TTS_Server.close()

class TTSResponse(BaseModel):
    voice_id:str
    text:str
    sr:int
    sdp_ratio:Optional[float] = 0.2
    noise_scale:Optional[float] = 0.6
    noise_scale_w:Optional[float] =  0.8
    speed:Optional[float] = 1.0

app = FastAPI(lifespan=lifespan)



@app.post("/connection")
def tts_process(response:TTSResponse):
    __t = time.time()
    audio, sr = TTS_Server.synthesize(response.text,speaker_id=speaker_ids[response.voice_id], sdp_ratio=response.sdp_ratio, noise_scale=response.noise_scale, noise_scale_w=response.noise_scale_w, speed=response.speed)
    audio = torch.from_numpy(audio)
    resampler = T.Resample(sr, response.sr, dtype=audio.dtype)
    audio = resampler(audio)
    audio = audio.detach().numpy()
    files = write_bytesIO(response.sr,audio)
    return {'audio': b64encode(files.read()).decode(),'sr':response.sr,"time":time.time() - __t}




if __name__ == "__main__":
    uvicorn.run("Server:app",host='0.0.0.0',port=8000,reload=True)