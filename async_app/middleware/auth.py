from aiohttp_session import get_session
from sqlalchemy.exc import NoResultFound

from async_app.models import User


async def auth_middleware(app, handler):

    async def middleware_wrapper(request):
        # ==========================================
        request.session = await get_session(request)  # Ожидаем получение сессий с Redis.
        request.user = None

        user_id = request.session.get('user_id')
        if user_id is not None:
            try:
                request.user = await User.get(_id=user_id)
            except NoResultFound:
                pass
        # ==========================================

        return await handler(request)

    return middleware_wrapper
