import sqlalchemy
from aiohttp import web
from aiohttp_jinja2 import template
from sqlalchemy.exc import NoResultFound
from .models import Post, User


class HomeView(web.View):
    @template("home.html")
    async def get(self):
        all_posts = await Post.all()
        print(all_posts)
        username = self.request.user.username if self.request.user else "Anonymous"

        return {"title": "Hello World", "user": username, "posts": all_posts}


class NoteRedactView(web.View):
    @template("notes/update.html")
    async def get(self):
        post_id = int(self.request.match_info.get('post_id', -1))
        post = await Post.get_by_id(post_id)
        return {"post": post}

    @template("notes/update.html")
    async def post(self):
        post_id = int(self.request.match_info.get('post_id', -1))
        post_data = await self.request.post()
        action = post_data.get('action')
        post = None
        if post_id != -1:
            title = post_data.get('title', '')
            content = post_data.get('content', '')
            user_id = int(post_data.get('user_id', -1))
            updated_post = await Post.update(post_id=post_id, title=title, content=content, user_id=user_id)
            if updated_post:
                raise web.HTTPFound(f"/")
            else:
                post = await Post.get_by_id(post_id)
        if not post:
            post = await Post.get_by_id(post_id)
        return {"post": post, "error": "Не удалось обновить заметку."}


class NoteCreateView(web.View):
    @template("notes/create_form.html")
    async def get(self):
        return {}

    @template("notes/create_form.html")
    async def post(self):
        user_data = await self.request.post()
        title = user_data.get('title')
        content = user_data.get('content')
        post = await Post.create(title=title, content=content, user_id=self.request.user.id)
        print(post)

        raise web.HTTPFound("/")


class RegisterView(web.View):
    @template("account/register.html")
    async def get(self):
        return {}

    @template("account/register.html")
    async def post(self):
        user_data = await self.request.post()
        username = user_data.get('username')
        password = user_data.get('password')
        email = user_data.get('email')
        password_confirm = user_data.get('password_confirm')

        if await User.get_existing_user(user_data.get("username")):
            return {"error": "username already taken"}

        if password != password_confirm:
            return {"error": "passwords don't match"}

        try:
            user = await User.create_user(username=username, email=email, password=password)

            return web.HTTPFound("/login")
        except sqlalchemy.exc.SQLAlchemyError as e:
            return {"error": "Database error"}


class LoginView(web.View):

    @template("account/login.html")
    async def get(self):
        return {}

    @template("account/login.html")
    async def post(self):
        user_data = await self.request.post()

        username = user_data.get('username')
        password = user_data.get('password')

        try:
            user = await User.get_valid_user(username, password)
        except NoResultFound:
            return {"error": "Invalid username or password"}

        self.request.session["user_id"] = user.id

        raise web.HTTPFound("/")

