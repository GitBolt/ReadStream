FROM python:3

COPY /api /main 

WORKDIR /main

RUN pip install fastapi uvicorn youtube_dl Pillow pytesseract
RUN apt-get update && apt-get install -y ffmpeg && sudo apt-get install -y tesseract-ocr

CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}