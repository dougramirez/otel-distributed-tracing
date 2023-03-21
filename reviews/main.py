import uuid
from datetime import datetime
from random import randint, random
from time import sleep
from uuid import UUID, uuid4

from fastapi import FastAPI, Request
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from pydantic import BaseModel, Field

from otel.common import configure_logger, configure_tracer

logger = configure_logger("reviews-api", "1.0.0")
tracer = configure_tracer("reviews-api", "1.0.0")


class ReviewBase(BaseModel):
    uuid: UUID | None = uuid4()
    created: datetime | None = datetime.now()


class ReviewResult(BaseModel):
    body: str | None = "I am a review."


class ReviewIn(BaseModel):
    body: str | None = Field(default=None, example="I am a review.")


class ReviewOut(ReviewBase):
    succeeded_at: datetime | None = datetime.now()
    result: ReviewResult | None = ReviewResult()


app = FastAPI()


def get_by_band_id(band_id: UUID) -> list:
    number_of_reviews = randint(1, 20)

    reviews = []
    if band_id == "553be815-76f3-49db-b9d7-caca4b23cc3e":
        for i in range(number_of_reviews):
            sleep(random())
            reviews.append(
                ReviewOut(
                    result=ReviewResult(
                        body=f"This is the review {i + 1} of {number_of_reviews} for this band."
                    )
                )
            )

    return reviews


@app.get("/health")
def health():
    with tracer.start_as_current_span("/health"):
        logger.info("/health has been called")

        return {"status": "ok"}


@app.get("/reviews/{id}", response_model=ReviewOut)
def get_review(request: Request, id: str):
    with tracer.start_as_current_span("/reviews/{id}"):
        logger.info("/reviews/{id} has been called")

        review_uuid = uuid.UUID(id)
        review = ReviewOut(uuid=review_uuid)

        return review


@app.get("/reviews", response_model=list[ReviewOut])
def get_reviews(request: Request, band_id: str):
    traceparent = request.headers.get("traceparent")
    carrier = {"traceparent": traceparent}
    trace_context = TraceContextTextMapPropagator().extract(carrier)

    with tracer.start_as_current_span("/reviews?band_id", context=trace_context):
        logger.info("/reviews?band_id has been called")

        with tracer.start_as_current_span("get reviews by band_id"):
            reviews = get_by_band_id(band_id)

            return reviews
