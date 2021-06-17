FROM python:3

COPY /api /main 

WORKDIR /main

RUN pip install fastapi uvicorn youtube_dl PIL pytesseract

CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}