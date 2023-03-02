# otel-distrbuted-tracing

## Setup
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip3 install fastapi
pip3 install uvicorn
pip3 install black
```

Start Jaeger
```sh
docker run --name jaeger \
  -e COLLECTOR_OTLP_ENABLED=true \
  -p 16686:16686 \
  -p 4317:4317 \
  -p 4318:4318 \
  jaegertracing/all-in-one:1.42.0
```

Set the environment variable for the Collector:
```sh
export OTEL_EXPORTER_OTLP_ENDPOINT="0.0.0.0:4317"
```

## Bands
Start the bands service
```sh
uvicorn bands.main:app --reload --port 8000
```

Make sure the bands service running
```sh
curl -w '\n' 127.0.0.1:8000/health
{"status":"ok"}

```

Get a band
```sh
curl -w '\n' 127.0.0.1:8000/bands/553be815-76f3-49db-b9d7-caca4b23cc3e
{"uuid":"553be815-76f3-49db-b9d7-caca4b23cc3e","created":"2023-03-02T08:13:28.502366","succeeded_at":"2023-03-02T08:13:28.502873","result":{"name":"Fugazi"}}

```

## Reviews
Start the reviews service
```sh
uvicorn reviews.main:app --reload --port 8080
```

Make sure the reviews service running
```sh
curl -w '\n' 127.0.0.1:8080/health
{"status":"ok"}

```

Get a review
```sh
curl -w '\n' 127.0.0.1:8080/reviews/553be815-76f3-49db-b9d7-caca4b23cc3e
{"uuid":"553be815-76f3-49db-b9d7-caca4b23cc3e","created":"2023-03-02T08:22:57.546341","succeeded_at":"2023-03-02T08:22:57.546772","result":{"body":"I am a review."}}

```