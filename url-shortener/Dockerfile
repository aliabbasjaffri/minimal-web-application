FROM tiangolo/uvicorn-gunicorn:python3.9

RUN mkdir -p /opt/api
WORKDIR /opt/api

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY templates/ templates/
COPY route/ route/
COPY utils/ utils/
COPY database/ database/
COPY tests/ tests/

EXPOSE 5000

# https://fastapi.tiangolo.com/deployment/server-workers/
ENTRYPOINT ["gunicorn" , "-k uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:5000", "--threads=2", "--workers=1", "main:app"]