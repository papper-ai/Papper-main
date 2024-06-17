FROM python:3.12.2-slim
LABEL authors="pomelk1n"

WORKDIR /usr/data/app

COPY requirements/base.txt requirements/
RUN apt-get update && apt-get install -y iputils-ping &&\
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements/base.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -r requirements

COPY . main_service/

ENV PYTHONPATH=/usr/data/app/

ENTRYPOINT ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "main_service/src/uvicorn-logging-config.yaml"]