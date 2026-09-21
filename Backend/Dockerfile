FROM python:3.11-slim

WORKDIR /app

COPY requirements-docker.txt .
RUN pip install --no-cache-dir -r requirements-docker.txt

COPY . .

EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
