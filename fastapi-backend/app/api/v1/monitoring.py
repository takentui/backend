from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

router = APIRouter()


@router.get(
    "/ping",
    responses={"200": {"content": {"application/json": {"example": {"status": "OK"}}}}},
    response_class=ORJSONResponse,
)
async def ping() -> ORJSONResponse:
    """Health check for service"""
    return ORJSONResponse({"status": "OK"})
