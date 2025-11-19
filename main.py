from fastapi import FastAPI, Response
import yt_dlp
import uuid
import os

app = FastAPI()

@app.get("/video")
def video(id: str):
    temp_name = f"/tmp/{uuid.uuid4()}.mp4"

    # Download video with yt-dlp
    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": temp_name,
        "quiet": True,
        "nocheckcertificate": True,
        "merge_output_format": "mp4"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"https://www.youtube.com/watch?v={id}"])

    # Check file exists
    if not os.path.exists(temp_name):
        return {"error": "Download failed"}

    file_size = os.path.getsize(temp_name)

    # Read file in binary
    with open(temp_name, "rb") as f:
        data = f.read()

    headers = {
        "Content-Type": "video/mp4",
        "Content-Disposition": "attachment; filename=video.mp4",
        "Content-Length": str(file_size),
        "Accept-Ranges": "bytes"
    }

    return Response(content=data, media_type="video/mp4", headers=headers)
