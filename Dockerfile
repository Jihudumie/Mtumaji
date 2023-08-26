# Kutumia msingi wa Python
FROM python:3.10

# Sakinisha Pyrogram
RUN pip install -r requirements.txt

# Weka directory ya kazi
WORKDIR /app

# Weka faili za bot kwenye directory ya kazi
COPY . /app

# Endesha bot yako
CMD ["python", "main.py"]
