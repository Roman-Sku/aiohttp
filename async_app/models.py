import bcrypt
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, select
from datetime import datetime
from .database.connector import db_conn
from .database.base import Base, Manager


class User(Base, Manager):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(300), nullable=False)
    email = Column(String(100), nullable=True)
    first_name = Column(String(100), nullable=False, default="")
    last_name = Column(String(100),nullable=False, default="")
    middle_name = Column(String(100), nullable=False, default="")

    def __str__(self):
        return f"User: {self.id} ({self.username})"

    @classmethod
    async def create_user(cls, **kwargs):
        password = kwargs.get("password")
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        kwargs["password"] = hashed_password
        return await super().create(**kwargs)

    @classmethod
    async def get_valid_user(self, username: str, password: str) -> "User":

        async with db_conn.session as session:
            query = select(User).where(User.username == username)
            data = await session.execute(query)
            user = data.scalar_one_or_none()

            if user and  bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                return user
            else:
                return None

    @classmethod
    async def get_existing_user(cls, username):
        async with db_conn.session as session:
            res = await session.execute(select(cls).where(cls.username == username))
            if res.scalar_one_or_none() is not None:
                return True
            else:
                return False


class Post(Base, Manager):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100))
    content = Column(Text())
    created = Column(DateTime(), default=datetime.now)
    user_id = Column(ForeignKey("users.id", ondelete="cascade"))

    @classmethod
    async def get_by_id(cls, note_id: int) -> "Post":
        async with db_conn.session as session:
            query = select(Post).where(Post.id == note_id)
            data = await session.execute(query)
            post = data.scalar_one_or_none()
            return post

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Post: {self.title}>"
