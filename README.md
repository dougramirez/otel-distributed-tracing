# otel-distrbuted-tracing

## Goals

- Understand distributed tracing and context propagation concepts
- Know there is a W3C recommendation
- See a minimal example of distributed tracing in action
- Be aware of security implications

1. What is distrubuted tracing?
2. What is context propagation?
3. What are the elements of a trace context?
   1. traceparent
      1. `trace-id`
         1. [Globally Unique](https://www.w3.org/TR/trace-context/#uniqueness-of-trace-id)
         2. [Random](https://www.w3.org/TR/trace-context/#randomness-of-trace-id)
      2. `span-id`
      3. `parent-id`
   2. tracestate
4. Returning `trace-id`

## Quickstart

1. Start Jaeger in a Docker container
2. Start the `bands` service
3. Start the `reviews` service
4. Hit a `bands` endpoint and see the traces in [Jaeger](http://localhost:16686/search)

## Setup

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip3 install black
pip3 install isort
pip3 install fastapi
pip3 install uvicorn
pip3 install opentelemetry-sdk
pip3 install opentelemetry-exporter-otlp-proto-grpc
pip3 install httpx
```

Start Jaeger
```sh
docker run --name jaeger \
  -e COLLECTOR_OTLP_ENABLED=true \
  -p 16686:16686 \
  -p 4317:4317 \
  -p 4318:4318 \
  jaegertracing/all-in-one:1.42
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