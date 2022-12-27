import json
import aiohttp
import asyncio
import aiosqlite
from aiohttp import web
import aiofiles

routes = web.RouteTableDef()
global DATABASE
DATABASE = "MiniProjekt1/db/database.db"

def parse_data(obj):
    item = (
        obj["repo_name"].split("/")[0],
        "https://github.com/" + obj["repo_name"],
        obj["path"].split("/")[-1],
    )
    return item

async def insert_into_db():
    async with aiofiles.open("MiniProjekt1/db/FakeDataset.json", mode = "r") as file:
        i = 0        
        async for line in file:
            async with aiosqlite.connect(DATABASE) as database:
                await database.execute(
                    "INSERT INTO eucenje (username, ghlink, filename) VALUES (?, ?, ?)",
                    parse_data(json.loads(line))
                )
                await database.commit()
            i += 1
            if i == 10000:
                return
        

async def check_db():
    async with aiosqlite.connect(DATABASE) as database:
        cursor = await database.cursor()
        await cursor.execute("SELECT COUNT(*) FROM eucenje")
        count = await cursor.fetchall()

        if count[0][0] == 0:
            await insert_into_db()


@routes.get("/getData")
async def get_data_db(request):
    try:
        await check_db()
        return web.json_response({ "Status": "ok" }, status = 200)
    
    except Exception as e:
        return web.json_response({ "Error": str(e) })


app = web.Application()

app.router.add_routes(routes)

web.run_app(app)