from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import yt_dlp
import uuid
import os

app = FastAPI()

@app.get("/video")
def video(id: str):
    temp_path = f"/tmp/{uuid.uuid4()}.mp4"

    # Download video using yt-dlp
    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": temp_path,
        "quiet": True,
        "nocheckcertificate": True,
        "merge_output_format": "mp4"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"https://www.youtube.com/watch?v={id}"])

    if not os.path.exists(temp_path):
        return {"error": "Video download failed"}

    file_size = os.path.getsize(temp_path)

    def iterfile():
        with open(temp_path, "rb") as f:
            while chunk := f.read(1024 * 1024):
                yield chunk
        os.remove(temp_path)  # cleanup

    headers = {
        "Content-Type": "video/mp4",
        "Content-Length": str(file_size),
        "Accept-Ranges": "bytes"
    }

    return StreamingResponse(iterfile(), media_type="video/mp4", headers=headers)
