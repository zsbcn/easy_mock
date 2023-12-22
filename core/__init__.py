import pkgutil
from importlib import __import__
from pathlib import Path

from fastapi import APIRouter
from loguru import logger

all_routers = APIRouter()

model_list = pkgutil.iter_modules(__path__)
for i in model_list:
    module = __import__(f'{Path(__file__).parent.name}.{i.name}', fromlist=[i.name])
    all_routers.include_router(getattr(module, "router"))
    logger.info(f"imported {i.name}")
