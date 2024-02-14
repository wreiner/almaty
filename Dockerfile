FROM python:3.9.18-slim-bookworm

COPY app /app
WORKDIR /app

RUN pip install -r /app/requirements.txt

EXPOSE 8000

ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:8000 --workers=1 --threads=1 --access-logfile=- --error-logfile=-"

# Run app.py when the container launches
CMD ["gunicorn", "app:app"]
