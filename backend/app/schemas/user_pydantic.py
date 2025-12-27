from pydantic import BaseModel, EmailStr, field_validator

class UserModel(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_check(cls, password: str):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return password

    @field_validator("email")
    @classmethod
    def email_check(cls, email: EmailStr):
        if not email.endswith("@gmail.com"):
            raise ValueError("Only Gmail addresses are allowed")
        return email
