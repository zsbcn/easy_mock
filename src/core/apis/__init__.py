import pkgutil
from importlib import import_module

from fastapi import APIRouter
from loguru import logger

all_routers = APIRouter()

# 自动加载core目录下的APIRouter
model_list = pkgutil.iter_modules(__path__)
for i in model_list:
    module = import_module(f'core.apis.{i.name}')
    all_routers.include_router(getattr(module, "router"))
    logger.info(f"imported {i.name}")
