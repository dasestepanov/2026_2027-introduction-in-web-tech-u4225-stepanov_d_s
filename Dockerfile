FROM python:3.9-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl vim \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Flask 2.0.1 requires the older Werkzeug API.
RUN pip install --no-cache-dir -r requirements.txt "Werkzeug==2.0.3"

COPY app.py .

RUN useradd --uid 1000 --create-home appuser
USER appuser

EXPOSE 5000
ENV FLASK_ENV=production

CMD ["python", "app.py"]
