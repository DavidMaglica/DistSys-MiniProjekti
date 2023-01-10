"""
2. WT microservis uzima dictionary. Uzima samo redove gdje username
pocinje na w. Prosljeduje kod 4. microservisu.
"""

import asyncio
import aiohttp
from aiohttp import web

routes = web.RouteTableDef()

def extract_workers_w(dict):
    result = []
    for k, v in enumerate(dict["usernames"]):
        if v[0].lower() == "w":
            result.append({
                "filename": dict["filenames"][k],
                "content": dict["content"][k]
            })
    return result

@routes.post("/WT_w")
async def worker_tokenizer(request):
    try:
        req = await request.json()
        async with aiohttp.ClientSession() as session:
            res = await session.post(
                "http://localhost:8084/gatherData",
                json = extract_workers_w(req["data"])
            )

            res.close()

        return web.json_response({ "service_id": 2, "status": "ok"}, status = 200)

    except Exception as e:
        return web.json_response({ "service_id": 2, "Error": str(e) }, status = 500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port = 8082)