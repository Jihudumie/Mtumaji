# Kutumia msingi wa Python
FROM python:3.9-slim

# Weka jina la mtengenezaji
LABEL maintainer="Jina Lako"

# Weka mazingira ya lugha kwa default UTF-8
ENV LANG C.UTF-8

# Weka variables za mazingira kwa ajili ya API_ID, API_HASH, na BOT_TOKEN
ENV API_ID your_api_id
ENV API_HASH your_api_hash
ENV BOT_TOKEN your_bot_token

# Weka variables za mazingira kwa ajili ya vikao vya Pyrogram
ENV SESSION_NAME Mtumaji

# Sakinisha vifurushi vya msingi
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Sakinisha Pyrogram
RUN pip install pyrogram==1.2.8

# Weka directory ya kazi
WORKDIR /app

# Weka faili za bot kwenye directory ya kazi
COPY . /app

# Endesha bot yako
CMD ["python", "main.py"]
