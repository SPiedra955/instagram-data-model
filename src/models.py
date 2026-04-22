from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(
        String(120), unique=False, nullable=False)
    first_name: Mapped[str] = mapped_column(
        String(120), unique=False, nullable=False)
    last_name: Mapped[str] = mapped_column(
        String(120), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    follower = relationship(back_populates="user_from_id")

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Follower(db.Model):
    __tablename__ = "follower"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[User] = relationship(back_populates="user")
    user_to_id: Mapped[int] = mapped_column(unique=False, nullable=False)

    def serialize(self):
        return {
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }
