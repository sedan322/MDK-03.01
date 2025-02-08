#(©)Codexbotz
#@iryme

from aiohttp import web
from .route import routes
## web_server настраивает веб приложения для работы бота
async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app
