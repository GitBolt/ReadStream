import os
from PIL import Image, ImageFilter
from fastapi import FastAPI
from youtube_dl import YoutubeDL
from pytesseract import pytesseract

import numpy as np

app = FastAPI()

ydl = YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})


def get_now_playing(filename, stream_url, crop_res):
    with ydl:
        result = ydl.extract_info(
            stream_url, 
            download=False
        )
    url = result["url"]
    os.system(f"ffmpeg -i {url} -f image2 -frames:v 1 {filename}")
    img = Image.open(filename).crop(crop_res).convert("RGB")


    datas = img.getdata()
    new_image_data = []

    for item in datas:
        if item[0] not in list(range(195, 256)):
            new_image_data.append((0, 0, 0))
        else:
            new_image_data.append(item)
    img.putdata(new_image_data)
    img.filter(ImageFilter.GaussianBlur(radius = 100))

    #img.save("test.png")
    os.remove(filename)

    text = pytesseract.image_to_string(img, lang='eng')
    filtered = text[:-1].split("\n")[0]
    return filtered



@app.get("/")
async def index():
    return {
        "Welcome!": "👋",
        "Beats to relax/study": "/1",
        "Beats to sleep/chill": "/2"
    }


@app.get("/1")
async def index():

    now_playing = get_now_playing("stream1.png", "https://www.youtube.com/watch?v=5qap5aO4i9A", (0, 0, 2000, 75))
    return now_playing


@app.get("/2")
async def index():

    now_playing = get_now_playing("stream2.png", "https://www.youtube.com/watch?v=DWcJFNfaw9c", (0, 0, 2000, 60))
    return now_playing
