"""
1. Microservis asinkrono poziva e-ucenje API (M1), te prosljeduje podatke
kao dictionary Worker tokenizer (WT) microservisu.

Proširen Fake M1. Nakon što dobije kolekciju URL-ova asinkrono preuzima
repozitorije sa zadacama. Asinkrono asinkrono cita red po red Python
datoteke (M1+), te prosljeđuje stringove WTMs.
"""

import aiohttp
import asyncio
from aiohttp import web
from git import Repo


routes = web.RouteTableDef()

async def get_100(session, offset):
    result = await session.get(f"http://localhost:8080/getDataDb?offset={offset}")
    
    return await result.json()

async def git_clone(url):
    for i in range(len(url)):
        item = url[i].split("/")[-1]
        repo_dir = f"MiniProjekt1/repos/{item}"
        Repo.clone_from(url[i], repo_dir)

@routes.get("/getData")
async def get_data(request):
    try:
        tasks = []
        async with aiohttp.ClientSession() as session:
            for i in range(0, 10001, 100):
                worker_tokenizer = await get_100(session, i)
                
                # await git_clone(worker_tokenizer["data"]["githubLinks"]) ova linija klonira cijeli repozitorij
    
                tasks.append(asyncio.create_task(session.post("http://localhost:8082/WT_w", json = worker_tokenizer)))
                tasks.append(asyncio.create_task(session.post("http://localhost:8083/WT_d", json = worker_tokenizer)))


                response = await asyncio.gather(*tasks)
                data = [await data.json() for data in response]
                

        return web.json_response({ "service_id": 1, "data": data }, status = 200)

    except Exception as e:
        return web.json_response({ "service_id": 1, "Error": str(e) })

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port = 8081)