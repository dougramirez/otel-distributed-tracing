import uuid
from datetime import datetime
from uuid import UUID, uuid4

from fastapi import FastAPI, Request
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


@app.get("/health")
def health():
    with tracer.start_as_current_span("/health"):
        logger.info("/health has been called")

    return {"status": "ok"}


@app.get("/reviews/{id}", response_model=ReviewOut)
def get_trace(request: Request, id: str):
    review_uuid = uuid.UUID(id)
    review = ReviewOut(uuid=review_uuid)

    return review
