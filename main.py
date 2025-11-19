from fastapi import FastAPI
from fastapi.responses import FileResponse
import yt_dlp
import uuid
import os

app = FastAPI()

@app.get("/video")
def video(id: str):
    out = f"{uuid.uuid4()}.mp4"
    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": out,
        "quiet": True,
        "nocheckcertificate": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"https://www.youtube.com/watch?v={id}"])

    return FileResponse(out, media_type="video/mp4", filename="video.mp4")
