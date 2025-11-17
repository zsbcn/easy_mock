from fastapi import APIRouter

from conf import ResponseBody, CONFIG

router = APIRouter(prefix="/config", tags=["系统配置"])


@router.get("/methods", response_model=ResponseBody, response_model_exclude_none=True)
async def get_methods():
    return ResponseBody(data=CONFIG["support_methods"])
