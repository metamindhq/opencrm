FROM python:3.11.5-slim
LABEL authors="sumandas"

# Dockerfile to run local fastapi app
COPY . /app
WORKDIR /app

RUN apt-get update && apt-get install -y procps
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["uvicorn", "opencrm.main:app"]
EXPOSE 8000