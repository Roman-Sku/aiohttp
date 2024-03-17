from aiohttp import web

from async_app import views

routes = [
    web.get("/", handler=views.HomeView),
    web.route("*", "/login", handler=views.LoginView),
    web.route("*", "/register", handler=views.RegisterView),
    web.route("*", "/notes/create", handler=views.NoteCreateView),
    web.route("*", "/notes/update/{post_id}", handler=views.NoteRedactView),
]
