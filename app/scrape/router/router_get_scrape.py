from typing import Any, Optional
import structlog

from fastapi import Depends
from pydantic import Field

from app.utils import AppModel

from ...adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data
from bson import ObjectId


@router.get("/{scrape_id}")
def get_my_account(
    scrape_id: str,
    svc: Service = Depends(get_service),
):
    structlog.get_logger().error("start", d=scrape_id, s=str(scrape_id))
    scrape_data = svc.scrape_repository.get_scrape_data(str(scrape_id))
    structlog.get_logger().error("data", d=scrape_data)
    return scrape_data
