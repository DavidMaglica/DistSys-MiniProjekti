import aiosqlite
import asyncio
import aiohttp
import aiofiles
from aiohttp import web
import json
import os

routes = web.RouteTableDef()

@routes.get("/getData")
async def get_data_db(request):
    try:
        async with aiofiles.open("MiniProjekt1/FakeDataset.json", mode='r') as file_data:
            

            # TODO change 10 to 10_000
            read_data = {await file_data.readline() for _ in range(10)}

            whole_data = [json.loads(line) for line in read_data]

            data_to_db = []
            for item in whole_data:
                db_item = {}
                db_item["username"] = item["repo_name"] # TODO slice str to keep just the username 
                db_item["ghlink"] = "https://github.com/" + item["repo_name"]
                db_item["filename"] = item["path"] # TODO slice str to keep just the file name 
                data_to_db.append(db_item)

        return web.json_response(data_to_db, status = 200)

    except Exception as e:
        return web.json_response({ "Error": str(e) }, status = 500)


# async def populate_db():
#     db = await aiosqlite.connect("MiniProjekt1/projekt.db")
#     cursor = await db.execute(
#         "CREATE TABLE fakeDataset (id INTEGER PRIMARY KEY AUTOINCREMENT, usename STRING, ghlink STRING, filename STRING"
#     )
#     with open ("FakeDataset.json") as dataset:
#         data = dataset.readlines()
    
#     data = {dict(line.strip().split("m")) for line in data}

#     await cursor.executemany("INSERT into fakeDataset VALUES (?, ?, ?, ?)", data)
#     await db.commit()
#     await cursor.close()
#     await db.close

app = web.Application()

app.router.add_routes(routes)

web.run_app(app)