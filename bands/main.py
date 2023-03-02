import uuid
from datetime import datetime
from uuid import UUID, uuid4

from fastapi import FastAPI, Request
from pydantic import BaseModel, Field

from otel.common import configure_logger, configure_tracer

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


app = FastAPI()


@app.get("/health")
def health():
    with tracer.start_as_current_span("/health"):
        logger.info("/health has been called")

    return {"status": "ok"}


@app.get("/bands/{id}", response_model=BandOut)
def get_band(request: Request, id: str):
    with tracer.start_as_current_span("/bands/{id}"):
        logger.info("/bands/{id} has been called")

        band_uuid = uuid.UUID(id)
        band = BandOut(uuid=band_uuid)

        return band
