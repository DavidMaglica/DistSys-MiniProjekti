import aiosqlite
import asyncio
import aiohttp
import aiofiles
from aiohttp import web
import json

routes = web.RouteTableDef()

@routes.get("/getData")
async def get_data_db(request):
    try:
        async with aiosqlite.connect("MiniProjekt1/projekt.db") as database:
            cursor = await database.cursor()

            await cursor.execute("SELECT * FROM Projekt1")

            results = await cursor.fetchall()

            # IF empty need to fill with first 10_000 lines from FakeDataset.json
            if results == []:
                async with aiofiles.open("MiniProjekt1/FakeDataset.json", mode='r') as file_data:
                    raw_data = {await file_data.readline() for _ in range(20)}

                    json_data = [json.loads(line) for line in raw_data]

                    db_data = [
                        {
                            "username": item["repo_name"].rsplit("/", 1)[0],
                            "ghlink": "https://github.com/" + item["repo_name"],
                            "filename": item["path"].rsplit("/", 1)[1]
                        }
                        for item in json_data
                    ]

                    await populate_db(db_data)

            # ELSE grab max 100 lines of data from DB      
            else: 
                print(results)

        return web.json_response("ok", status = 200)

    except Exception as e:
        return web.json_response({ "Error": str(e) }, status = 500)


async def populate_db(data_list):
    async with aiosqlite.connect("MiniProjekt1/projekt.db") as db:
        cursor = await db.cursor()

        keys = ", ".join([key for key in data_list[0].keys() if key != "id"])
        placeholders = ", ".join("?" for _ in data_list[0].values())
        sql_insert = f"INSERT INTO Projekt1 ({keys}) VALUES ({placeholders})"

        values = [[v for k, v in item.items() if k != "id"] for item in data_list]
        await cursor.executemany(sql_insert, values)

        await db.commit()


app = web.Application()

app.router.add_routes(routes)

web.run_app(app)