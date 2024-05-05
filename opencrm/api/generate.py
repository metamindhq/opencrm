import os
from fastapi import APIRouter
import google.generativeai as genai
from typing import Annotated
from magika import Magika
from fastapi import File

router = APIRouter(
    prefix="/generate",
    tags=["generate"]
)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", None)
if GOOGLE_API_KEY is None:
    raise ValueError("API key not found")

genai.configure(api_key=GOOGLE_API_KEY)


@router.post("/audio")
async def generate_audio(prompt: str, audio_file: Annotated[bytes, File()]):
    file_name = f"{len(audio_file)}.mp3"
    file_content = await audio_file.read()
    # verify it is audio file
    magika = Magika()
    result = magika.identify_bytes(file_content)
    if result.output.ct_label != "audio":
        return {"error": "Invalid audio file"}
    # store the audio in file
    with open(file_name, "wb") as f:
        f.write(file_content)
    # generate audio
    file = genai.upload_file(file_name)
    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
    response = model.generate_content([prompt, file])
    return response

@router.post("/text")
