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

Here's an example of a `traceparent` header:

```sh
traceparent: 00-82d7195881bcb9de88498cfd59d9a6f7-cd713b8ff16363f4-01
```

### `tracestate`

The `tracestate` header provides a mechanism to share additional information about a trace.  It's simply a list of key/value pairs.

Here's an example of a `tracestate` header:

```sh
tracestate: foo=bar
```

### Privacy

Please familiarize yourself with the W3C's [Privacy Considerations](https://www.w3.org/TR/trace-context/#privacy-considerations).

## Demo

1. Start the services
2. Make a call
3. Add tracing to `bands-api`
4. Add Context Propagation to caller
5. Make a call
6. Add tracing to `reviews-api`
7. Make a call
8. Debug performance issue
9.  Fix bugs
10. Make a call

## Next Steps
- Test the documentation
- Add code comments to explain what the OTel SDK is doing
- Add `trace-id` to Response header
- Add `tracestate` to demo
- Add trace log correlation

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

### Jaeger

Start Jaeger

```sh
docker run --name jaeger \
  -e COLLECTOR_OTLP_ENABLED=true \
  -p 16686:16686 \
  -p 4317:4317 \
  -p 4318:4318 \
  jaegertracing/all-in-one:latest
```

### `bands-api`

Start `bands-api`

```sh
uvicorn bands.main:app --reload --port 8000
```

### `reviews-api`

Start `reviews-api`

```sh
uvicorn reviews.main:app --reload --port 8080
```

### Get a band and its reviews
```sh
python3 run.py   
{
    "uuid": "553be815-76f3-49db-b9d7-caca4b23cc3e",
    "name": "Fugazi",
    "reviews": [
        {
            "uuid": "ff8e9267-0b4d-47fa-abc7-4f112c533186",
            "body": "This is the review 1 of 3 for this band.",
            "created": "2023-03-30T10:33:58.886900"
        },
        {
            "uuid": "ff8e9267-0b4d-47fa-abc7-4f112c533186",
            "body": "This is the review 2 of 3 for this band.",
            "created": "2023-03-30T10:33:58.886900"
        },
        {
            "uuid": "ff8e9267-0b4d-47fa-abc7-4f112c533186",
            "body": "This is the review 3 of 3 for this band.",
            "created": "2023-03-30T10:33:58.886900"
        }
    ],
    "created": "2023-03-30T10:33:58.897368"
}
http://localhost:16686/trace/46d714dca76ce65b8b13881cf7b1488a
```

## Resources

- [OpenTelemetry](https://opentelemetry.io)
- [W3C Trace Context](https://www.w3.org/TR/trace-context)
- [Jaeger](https://www.jaegertracing.io)
