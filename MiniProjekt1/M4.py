"""
4. microservis sastoji od rute (/gatherData) sprema se Python kod u listu.
Ako ima više od 10 elemenata unutar liste asinkrono se kreiraju svi file-ovi
iz liste.
"""

import aiohttp
from aiohttp import web
import asyncio
import aiofiles

routes = web.RouteTableDef()

global GATHERED_DATA
GATHERED_DATA = []

@routes.post("/gatherData")
async def gather_data(request):
    req = await request.json()
    GATHERED_DATA.extend(req)
    print("len:", len(GATHERED_DATA))
    i = 0
    for _ in GATHERED_DATA:
        print(GATHERED_DATA[i]["username"])
        i += 1

    return web.json_response({ "status": "ok", "data": req }, status = 200)


app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port = 4)