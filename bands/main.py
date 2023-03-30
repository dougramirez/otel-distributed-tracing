import uuid
from datetime import datetime
from uuid import UUID, uuid4

import httpx
from fastapi import FastAPI, Request
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from pydantic import BaseModel, Field

from otel.common import configure_tracer

tracer = configure_tracer("bands-api", "1.0.0")

app = FastAPI()


class Band(BaseModel):
    uuid: UUID | None = uuid4()
    name: str | None = "Fugazi"
    reviews: list | None = []
    created: datetime | None = datetime.now()


def get_reviews(band_id: str) -> list:
    with tracer.start_as_current_span("get_reviews"):
        carrier = {}
        TraceContextTextMapPropagator().inject(carrier)
        headers = carrier
        with httpx.Client() as client:
            reviews = client.get(
                f"http://127.0.0.1:8080/reviews?band_id={band_id}",
                timeout=30.0,
                headers=headers,
            )

    return reviews.json()


@app.get("/bands/{id}", response_model=Band)
def get_band(request: Request, id: str):
    traceparent = request.headers.get("traceparent")
    carrier = {"traceparent": traceparent}
    trace_context = TraceContextTextMapPropagator().extract(carrier)
    with tracer.start_as_current_span("GET /bands/:id", context=trace_context):
        band_uuid = uuid.UUID(id)
        band = Band(uuid=band_uuid)
        band.reviews = get_reviews(id)

        return band
