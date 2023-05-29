from uuid import uuid4
from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext

from server import config
from server.db import auth_redis, get_session
from customers.models import Customer
from customers.schemas import SignUpModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)


async def get_customer_by_phone(db: AsyncSession, phone: str) -> Customer:
    result = await db.execute(select(Customer).filter_by(phone=phone))
    awaited_result = result.scalars().first()
    return awaited_result


async def create_customer(sign_up: SignUpModel) -> Customer:
    password = hash_password(sign_up.password1)
    async with get_session() as db:
        customer = Customer(name=sign_up.name, phone=sign_up.phone, password=password)
        db.add(customer)
        await db.commit()
        await db.refresh(customer)
    return customer


def generate_cookie(customer_id: int) -> str:
    cookie = str(uuid4())
    auth_redis.set(customer_id, cookie)
    auth_redis.expire(customer_id, timedelta(weeks=config.COOKIE_EXPIRE_WEEKS))
    return cookie
