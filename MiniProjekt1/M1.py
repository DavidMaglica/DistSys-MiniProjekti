"""
1. Microservis asinkrono poziva e-ucenje API (M1), te prosljeduje podatke
kao dictionary Worker tokenizer (WT) microservisu.
"""

import aiohttp
import asyncio
from aiohttp import web

routes = web.RouteTableDef()

@routes.get("/getData")
async def get_data(request):
    try:
        tasks = []
        async with aiohttp.ClientSession() as session:
            res = await session.get("http://localhost:1/getDataDb?offset=0")
            worker_tokenizer = await res.json()

            tasks.append(asyncio.create_task(session.post("http://localhost:3/WT", json = worker_tokenizer)))

            response = await asyncio.gather(*tasks)
            data = [await data.json() for data in response]

        return web.json_response({ "service_id": 1, "data": data }, status = 200)

    except Exception as e:
        return web.json_response({ "Error": str(e) })

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port = 2)