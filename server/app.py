import asyncio
import logging

from fastapi import FastAPI

from server.db import CustomerBase, engine
from customers.models import Customer
from customers.views import auth

logger = logging.getLogger(__name__)


async def async_db_initial():
    logger.info("Create tables: (%s)", Customer)
    async with engine.begin() as conn:
        await conn.run_sync(CustomerBase.metadata.create_all)


loop = asyncio.get_running_loop()
loop.create_task(async_db_initial())


app = FastAPI()
app.include_router(auth.router)
