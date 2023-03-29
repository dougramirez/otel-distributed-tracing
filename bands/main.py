import uuid
from datetime import datetime
from uuid import UUID, uuid4

import httpx
from fastapi import FastAPI, Request
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from pydantic import BaseModel, Field

from otel.common import configure_logger, configure_tracer

REVIEWS_API = "http://127.0.0.1:8080"

logger = configure_logger("bands-api", "1.0.0")
tracer = configure_tracer("bands-api", "1.0.0")


class BandBase(BaseModel):
    uuid: UUID | None = uuid4()
    created: datetime | None = datetime.now()


class BandResult(BaseModel):
    name: str | None = "Fugazi"


class BandIn(BaseModel):
    name: str | None = Field(default=None, example="Fugazi")


class BandOut(BandBase):
    succeeded_at: datetime | None = datetime.now()
    result: BandResult | None = BandResult()
    reviews: list | None = []


app = FastAPI()


@app.get("/health")
def health(
    request: Request,
):
    traceparent = request.headers.get("traceparent")
    print(f"traceparent: {traceparent}")
    carrier = {"traceparent": traceparent}
    trace_context = TraceContextTextMapPropagator().extract(carrier)
    print(trace_context)

    with tracer.start_as_current_span("GET /health", context=trace_context):
        logger.info("/health has been called")

        return {"status": "ok"}


@app.get("/bands/{id}", response_model=BandOut)
def get_band(request: Request, id: str):
    with tracer.start_as_current_span("GET /bands/:id"):
        logger.info("/bands/{id} has been called")

        band_uuid = uuid.UUID(id)
        band = BandOut(uuid=band_uuid)

        # Get the band's reviews
        with tracer.start_as_current_span("get_reviews"):
            # carrier = {}
            # TraceContextTextMapPropagator().inject(carrier)
            # headers = {"traceparent": carrier["traceparent"]}
            with httpx.Client() as client:
                reviews = client.get(
                    f"{REVIEWS_API}/reviews?band_id={id}",
                    timeout=30.0,
                    # headers=headers,
                )

                if reviews:
                    band.reviews = reviews.json()

            return band
