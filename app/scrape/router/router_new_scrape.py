from typing import Any
from uuid import uuid4
import structlog

from fastapi import Depends
from pydantic import Field

from app.utils import AppModel

from ...adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


class GetScrapeRequestIdResponse(AppModel):
    id: str


class ScrapeRequestForm(AppModel):
    scrape_url: str
    column_list: list[str]


class NewScrapeEvent(ScrapeRequestForm):
    scrape_id: str


@router.post("/new", response_model=GetScrapeRequestIdResponse)
def new_scrape_data(
    input: ScrapeRequestForm,
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    scrape_id = str(uuid4())
    new_scrape_event = NewScrapeEvent(
        scrape_id=scrape_id,
        scrape_url=input.scrape_url,
        column_list=input.column_list
    )
    structlog.get_logger().error("Init", s=input)
    svc.queue_new_scrape(new_scrape_event)
    return GetScrapeRequestIdResponse(id=scrape_id)
