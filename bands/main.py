import uuid
from datetime import datetime
from uuid import UUID, uuid4

import httpx
from fastapi import FastAPI, Request
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from pydantic import BaseModel, Field

from otel.common import configure_tracer

REVIEWS_API = "http://127.0.0.1:8080"
tracer = configure_tracer("bands-api", "1.0.0")

app = FastAPI()


class Band(BaseModel):
    uuid: UUID | None = uuid4()
    name: str | None = "Fugazi"
    reviews: list | None = []
    created: datetime | None = datetime.now()


@app.get("/health")
def health(request: Request):
    traceparent = request.headers.get("traceparent")
    carrier = {"traceparent": traceparent}
    trace_context = TraceContextTextMapPropagator().extract(carrier)
    with tracer.start_as_current_span("GET /health", context=trace_context):
        return {"status": "ok"}


@app.get("/bands/{id}", response_model=Band)
def get_band(request: Request, id: str):
    with tracer.start_as_current_span("GET /bands/:id"):
        band_uuid = uuid.UUID(id)
        band = Band(uuid=band_uuid)

        # Get the band's reviews
        with tracer.start_as_current_span("get_reviews"):
            carrier = {}
            TraceContextTextMapPropagator().inject(carrier)
            headers = {"traceparent": carrier["traceparent"]}
            with httpx.Client() as client:
                reviews = client.get(
                    f"{REVIEWS_API}/reviews?band_id={id}",
                    timeout=30.0,
                    headers=headers,
                )

                if reviews:
                    band.reviews = reviews.json()

        return band
