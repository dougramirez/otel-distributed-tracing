import uuid
from datetime import datetime
from random import randint, random
from time import sleep
from uuid import UUID, uuid4

from fastapi import FastAPI, Request
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from pydantic import BaseModel, Field

from otel.common import configure_tracer

tracer = configure_tracer("reviews-api", "1.0.0")

app = FastAPI()


class Review(BaseModel):
    uuid: UUID | None = uuid4()
    body: str | None = "I am a review."
    created: datetime | None = datetime.now()


def get_by_band_id(band_id: UUID) -> list:
    number_of_reviews = randint(1, 20)

    reviews = []
    if band_id == "553be815-76f3-49db-b9d7-caca4b23cc3e":
        for i in range(number_of_reviews):
            sleep(random())
            reviews.append(
                Review(
                    result=Review(
                        body=f"This is the review {i + 1} of {number_of_reviews} for this band."
                    )
                )
            )

    return reviews


@app.get("/health")
def health(request: Request):
    traceparent = request.headers.get("traceparent")
    carrier = {"traceparent": traceparent}
    trace_context = TraceContextTextMapPropagator().extract(carrier)
    with tracer.start_as_current_span("GET /health", context=trace_context):
        return {"status": "ok"}


@app.get("/reviews", response_model=list[Review])
def get_reviews(request: Request, band_id: str):
    traceparent = request.headers.get("traceparent")
    carrier = {"traceparent": traceparent}
    trace_context = TraceContextTextMapPropagator().extract(carrier)

    with tracer.start_as_current_span("GET /reviews?:band_id", context=trace_context):
        with tracer.start_as_current_span("get_by_band_id"):
            reviews = get_by_band_id(band_id)

            return reviews
