from fastapi import APIRouter
from fastapi.responses import JSONResponse, RedirectResponse, Response

from server.db import get_session
from customers.schemas import SignUpModel, SignInModel, Customer
from customers.utils import (
    get_customer_by_phone,
    get_customer_by_id,
    create_customer,
    generate_cookie,
)

router = APIRouter()


@router.post("/api/v1/signup")
async def signup(sign_up_data: SignUpModel):
    if await get_customer_by_phone(db=get_session(), phone=sign_up_data.phone):
        content = {"phone": "Номер уже зарегистрирован."}
        return JSONResponse(status_code=400, content=content)

    new_customer = await create_customer(sign_up_data)
    if not new_customer:
        return JSONResponse(status_code=500, content={"Internal Server Error": "500"})

    cookie = generate_cookie(customer_id=new_customer.id)
    content = {"id": new_customer.id, "phone": new_customer.phone}
    response = JSONResponse(status_code=201, content=content)
    response.set_cookie(key="sessionID", value=cookie)
    return response


@router.post("/api/v1/signin")
async def signin(sign_in_data: SignInModel):
    customer_ = await get_customer_by_phone(db=get_session(), phone=sign_in_data.phone)
    if not customer_:
        content = {"error": "Пользователя не существует."}
        return JSONResponse(status_code=400, content=content)

    cookie = generate_cookie(customer_id=customer_.id)
    response = Response(status_code=200)
    response.set_cookie(key="sessionID", value=cookie)
    return response


@router.get("/api/v1/customer/{customer_id}")
async def customer(customer_id: int):
    customer_ = await get_customer_by_id(customer_id)
    if not customer_:
        content = {"error": "Пользователя не существует"}
        return JSONResponse(status_code=404, content=content)
    content = Customer.from_orm(customer_).dict()
    return JSONResponse(status_code=200, content=content)


@router.delete("/api/v1/customer/{customer_id}")
async def customer_delete(customer_id: int):
    customer_ = await get_customer_by_id(customer_id)
    if not customer_:
        content = {"error": "Пользователя не существует"}
        return JSONResponse(status_code=404, content=content)

    async with get_session() as db:
        customer_.is_active = False
        await db.commit()
    content = {"id": customer_id}
    return JSONResponse(status_code=204, content=content)
