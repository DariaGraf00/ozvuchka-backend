from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import io

app = FastAPI()

origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "sk_e46be3f28ef39c89677d6132f0f4a0d23d4fb03241d9f802"

@app.get("/voices")
async def get_voices():
    """Этот endpoint возвращает список голосов."""
    headers = {
        "xi-api-key": API_KEY,
    }

    response = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers)

    if response.status_code == 200:
        return response.json()  # Отправляем список голосов
    else:
        return {"error": "Failed to retrieve voices"}

@app.post("/synthesize")
async def synthesize(request: Request):
    """Этот endpoint озвучивает переданный текст с выбранным голосом."""
    body = await request.json()
    text = body.get("text")
    voice_id = body.get("voice_id")

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return StreamingResponse(io.BytesIO(response.content), media_type="audio/mpeg")
    else:
        return {"error": "Failed to synthesize speech"}
