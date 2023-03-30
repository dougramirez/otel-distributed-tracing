# otel-distributed-tracing

## Goals

1. Introduce Distributed Tracing and Context Propagation concepts
2. See a minimal example of Distributed Tracing in action
3. Share some resources to learn more about Distributed Tracing

## Concepts

- What is Distributed Tracing?
  - An Observability concept that gives us the big picture of how a myriad of services interact with each other.
- What is Context Propagation?
  - The mechanism that allows services to share information with each other to identify a request that traverses code within and across services.  Context Propagation is what enables Distributed Tracing.
- What is a span?
  - A span is an operation or a unit of work.  A database query would be a good example of a span.
  - Each span has a unique identifier and is connected to a trace.
- What is a trace?
  - A trace is a collection of spans that tell the story of how a request traverses code within and across services.
  - Each trace has a unique identifier and is connected to a trace.
  - A `trace-id` should be [globally unique](https://www.w3.org/TR/trace-context/#uniqueness-of-trace-id) and [random](https://www.w3.org/TR/trace-context/#randomness-of-trace-id).
- What is Trace Context?
  - Trace Context provides a specification so that services have a mutually agreed upon format for sharing traces across service boundaries.

## W3C Recommendation

Fortunately, the W3C provides a specification for [Trace Context](https://www.w3.org/TR/trace-context).  This specification solves the problem of defining the format that all parties must agree to in order to share trace information across service boundaries.

The W3C recommends using two HTTP headers to share context:

   1. [`traceparent`](https://www.w3.org/TR/trace-context/#traceparent-header)
   2. [`tracestate`](https://www.w3.org/TR/trace-context/#tracestate-header)

### `traceparent`

The `traceparent` header is made up of four fields separated by a `-`:

1. `version`
2. `trace-id`
   1. A 16 byte array
3. `parent-id` (the `span-id` of the caller)
   1. An 8 byte array
4. `trace-flags`

Here's an example of a `traceparent`:

```sh
00-82d7195881bcb9de88498cfd59d9a6f7-cd713b8ff16363f4-01
```

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

## Resources

https://opentelemetry.io
https://www.w3.org/TR/trace-context
https://www.jaegertracing.io
