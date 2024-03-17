from aiohttp import web
import jinja2
import aiohttp_jinja2

from async_app.urls import routes
from async_app.database.connector import db_conn
from async_app.middleware.storage import session_storage_middleware
from async_app.middleware.auth import auth_middleware


async def init_db(app):
    print("Initializing database")
    db_conn.initialize("sqlite+aiosqlite:///db.sqlite3")


if __name__ == '__main__':
    app = web.Application(
        middlewares=[
            session_storage_middleware,
            auth_middleware
        ]
    )
    app.add_routes(routes)

    # При старте приложения будет выполнена корутина.
    app.on_startup.append(init_db)

    # Где расположены шаблоны.
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

    web.run_app(app, host='127.0.0.1', port=8001)
