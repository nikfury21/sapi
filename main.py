from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import yt_dlp
import uuid
import os

app = FastAPI()

@app.get("/video")
def get_video(id: str):
    temp_name = f"/tmp/{uuid.uuid4()}.mp4"

    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": temp_name,
        "quiet": True,
        "nocheckcertificate": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"https://www.youtube.com/watch?v={id}"])

    file_size = os.path.getsize(temp_name)

    def iterfile():
        with open(temp_name, "rb") as f:
            yield from f

    return StreamingResponse(
        iterfile(),
        media_type="video/mp4",
        headers={
            "Content-Disposition": "inline; filename=video.mp4",
            "Content-Length": str(file_size),
        },
    )
