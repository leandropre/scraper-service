FROM python:alpine

WORKDIR /app

COPY src/ .

RUN pip3 install -r requirements.txt

CMD ["python", "scraper_service.py"]
