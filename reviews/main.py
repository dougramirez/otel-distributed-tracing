import logging
from datetime import datetime
from random import randint, random
from time import sleep
from uuid import UUID, uuid4

from fastapi import FastAPI, Request
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from pydantic import BaseModel

from otel.common import configure_logger, configure_meter, configure_tracer

logger = configure_logger("reviews-api", "1.0.0")
logger.setLevel(logging.DEBUG)
meter = configure_meter("reviews-api", "1.0.0")
counter = meter.create_up_down_counter("reviews_fetched_counter")
tracer = configure_tracer("reviews-api", "1.0.0")

app = FastAPI()


class Review(BaseModel):
    uuid: UUID | None = uuid4()
    body: str | None = "I am a review."
    created: datetime | None = datetime.now()


def get_reviews_by_band_id(band_id: UUID) -> list:
    reviews = []
    with tracer.start_as_current_span("get_reviews_by_band_id"):
        number_of_reviews = randint(1, 20)

        if band_id == "553be815-76f3-49db-b9d7-caca4b23cc3e":
            for i in range(number_of_reviews):
                sleep(random())
                reviews.append(
                    Review(body=f"This is review {i + 1} of {number_of_reviews}.")
                )

        counter.add(number_of_reviews)

    return reviews


@app.get("/reviews", response_model=list[Review])
def get_reviews(request: Request, band_id: str):
    traceparent = request.headers.get("traceparent")
    carrier = {"traceparent": traceparent}
    trace_context = TraceContextTextMapPropagator().extract(carrier)
    with tracer.start_as_current_span("GET /reviews?:band_id", context=trace_context):
        logger.info("reviews service is getting reviews from local database")
        reviews = get_reviews_by_band_id(band_id)
        logger.info("reviews service got reviews from local database")

    return reviews
