from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from .base import BaseModel
from hashlib import sha256
from config import AppConfig


class UserModel(BaseModel):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    user_name: Mapped[str] = mapped_column(String(50), nullable=False)
    user_lastname: Mapped[str] = mapped_column(String(50), nullable=True)
    user_email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str]

    def __repr__(self):
        return f"UserModel(id={self.id}, username={self.username} , name={self.user_name}," \
               f"lastname={self.user_lastname}, email={self.user_email})"

    @staticmethod
    def hash_password(username, password):
        salted_password = f"{AppConfig.SALT_KEY}.{username}:{password}.{AppConfig.SALT_KEY}"
        hash_generator = sha256(salted_password.encode())
        return hash_generator.hexdigest()
