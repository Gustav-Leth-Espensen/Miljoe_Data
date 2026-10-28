FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY main_requirements.txt .
RUN pip install --no-cache-dir -r main_requirements.txt
COPY .. .

CMD ["python", "main.py"]