"""
2. WT microservis uzima dictionary. Uzima samo redove gdje username
pocinje na w. Prosljeduje kod 4. microservisu.

3. WT microservis uzima dictionary. Uzima samo redove gdje username
pocinje na d. Prosljeduje kod 4. microservisu.
"""

import asyncio
import aiohttp
from aiohttp import web

routes = web.RouteTableDef()

def extract_workers_d(d):
    result = []
    for x, y in enumerate(d["usernames"]):
        if y[0].lower() == "d":
            result.append({
                "username": y,
                "githubLink": d["githubLinks"][x],
                "filename": d["filenames"][x],
                "content": d["content"][x]
            })
    return result

def extract_workers_w(d):
    result = []
    for x, y in enumerate(d["usernames"]):
        if y[0].lower() == "w":
            result.append({
                "username": y,
                "githubLink": d["githubLinks"][x],
                "filename": d["filenames"][x],
                "content": d["content"][x]
            })
    return result

@routes.post("/WT")
async def worker_tokenizer(request):
    try:
        req = await request.json()
        tasks = []
        async with aiohttp.ClientSession() as session:
            tasks.append(asyncio.create_task(
                session.post("http://localhost:4/gatherData",
                json = extract_workers_w(req["data"]
            ))))
            
            tasks.append(asyncio.create_task(
                session.post("http://localhost:4/gatherData",
                json = extract_workers_d(req["data"]
            ))))

            await asyncio.gather(*tasks)
            await session.close()

        return web.json_response({ "service_id": 2, "status": "ok"}, status = 200)

    except Exception as e:
        return web.json_response({ "Error": str(e) }, status = 500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port = 3)