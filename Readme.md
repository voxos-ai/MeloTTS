# MeloTTS Server

This is TTS Server use [Melo TTS](https://github.com/myshell-ai/MeloTTS) as a base, We do some changes in the code base and created a FAST API server by which we get good performance for 100 chars we get response about `200~230 milliseconds latency` using G5 aws instance


### Install
```shell
python3 -m venv env
. ./env/bin/activate
pip install -r requirements.txt
python3 -m unidic download

```

### Server Start
```
python3 Server.py
```
### Request

```json
{
    "voice_id": "EN-US",
    "text": "Every morning, Sarah walked her dog, Max, through the old, enchanting forest near her home. One day, thanyou have a nice day",
    "sr": 8000,
    "sdp_ratio" : 0.2,
    "noise_scale" : 0.6,
    "noise_scale_w" :  0.8,
    "speed" : 1.0
}
```
there are 5 diffrent type of voices ids
- 'EN-US' 
- 'EN-BR' 
- 'EN-AU' 
- 'EN-Default' 
- 'EN_INDIA'
### Response
```json
{
    "audio": "audio file in base64",
    "sr": "audio sample rate",
    "time": "time required for genrate audio"
}
```