FROM python:3.10-slim 

# Доустановка ффмпега
RUN apt-get update && apt-get install -y \ 
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /bot

COPY requirements.txt ./
RUN pip install -r requirements.txt 
COPY . .

CMD ["python", "GoofyVoiceToTextbot.py"]

