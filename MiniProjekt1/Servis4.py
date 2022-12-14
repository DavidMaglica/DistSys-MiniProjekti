import aiosqlite
import aiohttp
from aiohttp import web

routes = web.RouteTableDef()

app = web.Application()

app.router.add_routes(routes)

web.run_app(app)