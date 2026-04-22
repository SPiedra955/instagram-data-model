from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
import enum
from sqlalchemy import Enum as SQLEnum

db = SQLAlchemy()


# ---------- ENUM ----------
class MediaType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"


# ---------- USER ----------
class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_name: Mapped[str] = mapped_column(String(120), nullable=False)
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)

    following: Mapped[List["Follower"]] = relationship(
        "Follower",
        foreign_keys="Follower.user_from_id",
        back_populates="user_from",
    )

    followers: Mapped[List["Follower"]] = relationship(
        "Follower",
        foreign_keys="Follower.user_to_id",
        back_populates="user_to",
    )

    # 1 user -> many posts
    posts: Mapped[List["Post"]] = relationship(
        "Post",
        back_populates="author"
    )

    # 1 user -> many comments
    comments: Mapped[List["Comment"]] = relationship(
        "Comment",
        back_populates="author"
    )

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        }


# ---------- FOLLOWER ----------
class Follower(db.Model):
    __tablename__ = "follower"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user_from: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_from_id],
        back_populates="following"
    )

    user_to: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_to_id],
        back_populates="followers"
    )

    def serialize(self):
        return {
            "id": self.id,
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }


# ---------- POST ----------
class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    author: Mapped["User"] = relationship(
        "User",
        back_populates="posts"
    )

    media: Mapped[List["Media"]] = relationship(
        "Media",
        back_populates="post"
    )

    comments: Mapped[List["Comment"]] = relationship(
        "Comment",
        back_populates="post"
    )


# ---------- MEDIA ----------
class Media(db.Model):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(primary_key=True)

    type: Mapped[MediaType] = mapped_column(
        SQLEnum(MediaType),
        nullable=False
    )

    url: Mapped[str] = mapped_column(String(200), nullable=False)

    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    post: Mapped["Post"] = relationship(
        "Post",
        back_populates="media"
    )


# ---------- COMMENT ----------
class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)

    comment_text: Mapped[str] = mapped_column(Text, nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    author: Mapped["User"] = relationship(
        "User",
        back_populates="comments"
    )

    post: Mapped["Post"] = relationship(
        "Post",
        back_populates="comments"
    )

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id
        }
