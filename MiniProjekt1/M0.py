"""
0. Fake E-ucenje API microservis (M0). Sastoji se od DB i jedne rute koja
vraca github linkove na zadace. Prilikom pokretanja servisa, provjerava
se postoje li podaci u DB. Ukoliko ne postoje, pokrece se funkcija koja
popunjava DB s testnim podacima (10000). Kad microservis zaprimi
zahtjev za dohvacanje linkova, uzima maksimalno 100 redataka podataka
iz DB-a.
"""

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
        obj["content"]
    )
    return item

async def insert_into_db():
    async with aiofiles.open("MiniProjekt1/db/FakeDataset.json", mode = "r") as file:
        i = 0        
        async for line in file:
            async with aiosqlite.connect(DATABASE) as database:
                await database.execute(
                    "INSERT INTO eucenje (username, ghlink, filename, content) VALUES (?, ?, ?, ?)",
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

@routes.get("/getDataDb")
async def get_data_db(request):
    try:   
        response = {
            "service_id": 0,
            "data": {
                "usernames": [],
                "githubLinks": [],
                "filenames": [],
                "content": []
            }
        }
    
        limit = 100
        offset = request.query["offset"]
        
        async with aiosqlite.connect(DATABASE) as database:
                async with database.execute(f"Select * FROM eucenje LIMIT {limit} OFFSET {offset}") as cursor:
                    async for row in cursor:
                        response["data"]["usernames"].append(row[1])
                        response["data"]["githubLinks"].append(row[2])
                        response["data"]["filenames"].append(row[3])
                        response["data"]["content"].append(row[4])

                        await database.commit()
                        print(f"i: {offset}")

        return web.json_response(response , status = 200)
    
    except Exception as e:
        return web.json_response({ "Error": str(e) })

asyncio.run(check_db())


app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port = 1)