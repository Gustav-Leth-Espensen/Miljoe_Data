FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ .

RUN addgroup --system appgroup && adduser --system --no-create-home --ingroup appgroup appuser
USER appuser
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]





