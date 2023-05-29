from pydantic import BaseModel, validator


class SignUpModel(BaseModel):
    name: str
    phone: str
    password1: str
    password2: str

    @validator('phone')
    def phone_length(cls, value):
        if len(value) != 10:
            raise ValueError("Введите корректный номер.")
        return value

    @validator('password2')
    def password_mismatch(cls, value, values):
        if 'password1' in values and value != values['password1']:
            raise ValueError("Пароли не совпадают.")
        return value


class SignInModel(BaseModel):
    phone: str
    password: str

    @validator('phone')
    def phone_length(cls, value):
        if len(value) != 10:
            raise ValueError("Введите корректный номер.")
        return value


class Customer(BaseModel):
    id: int
    name: str
    phone: str
    is_active: bool

    class Config:
        orm_mode = True
