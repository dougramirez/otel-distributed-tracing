import json
import logging

import httpx

from otel.common import configure_logger, configure_tracer

logger = configure_logger("client", "1.0.0")
logger.setLevel(logging.DEBUG)
tracer = configure_tracer("client", "1.0.0")


def get_trace_id(span) -> str:
    trace_id = format(span.get_span_context().trace_id, "032x")

    return trace_id


def get_span_id(span) -> str:
    span_id = format(span.get_span_context().span_id, "016x")

    return span_id


def create_headers(span) -> str:
    version = "00"
    trace_id = get_trace_id(span)
    span_id = get_span_id(span)
    trace_flags = "01"
    headers = {"traceparent": f"{version}-{trace_id}-{span_id}-{trace_flags}"}

    return headers


with tracer.start_as_current_span("get_band") as span:
    headers = create_headers(span)
    with httpx.Client() as client:
        logger.info("client is calling bands service API")
        band = client.get(
            "http://127.0.0.1:8000/bands/553be815-76f3-49db-b9d7-caca4b23cc3e",
            timeout=30.0,
            headers=headers,
        )
        logger.info("client received response from bands service API")

print(json.dumps(band.json(), indent=4))
print(f"http://localhost:3301/trace/{get_trace_id(span)}")
