import aiosqlite
import asyncio


class Database(object):
    async def create_table(self):
        async with aiosqlite.connect('../db/db.db') as db:
            await db.execute(
                "CREATE TABLE IF NOT EXISTS plans (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, username TEXT NOT NULL, date TEXT NOT NULL, time TEXT NOT NULL, event TEXT NOT NULL)")
            await db.commit()

    async def get_last_plan(self):
        async with aiosqlite.connect('./db/db.db') as db:
            cursor = await db.cursor()
            await cursor.execute("SELECT * FROM plans ORDER BY id DESC LIMIT 1")
            return await cursor.fetchone()

    async def add_plan(self, user_id: int, username: str, date: str, time: str, event: str):
        async with aiosqlite.connect('./db/db.db') as db:
            last = await self.get_last_plan()
            id = last[0] + 1 if last else 1
            await db.execute("INSERT INTO plans VALUES (?,?,?,?,?,?)", (id, user_id, username, date, time, event))
            await db.commit()

    async def delete_plan(self, user_id: int, date: str, time: str):
        async with aiosqlite.connect('./db/db.db') as db:
            await db.execute("DELETE FROM plans WHERE user_id = ? AND date = ? AND time =?", (user_id, date, time))
            await db.commit()

    async def get_plan(self, user_id: int, date: str, time: str):
        async with aiosqlite.connect('./db/db.db') as db:
            cursor = await db.cursor()
            await cursor.execute("SELECT * FROM plans WHERE user_id = ? AND date = ? AND time =?",
                                 (user_id, date, time))
            return await cursor.fetchone()

    async def get_plans_on_day(self, user_id: int, date: str):
        async with aiosqlite.connect('./db/db.db') as db:
            cursor = await db.cursor()
            await cursor.execute("SELECT username,time, event FROM plans WHERE user_id = ? AND date = ?",
                                 (user_id, date))
            return await cursor.fetchall()

    async def get_user_ids(self):
        async with aiosqlite.connect('./db/db.db') as db:
            cursor = await db.cursor()
            await cursor.execute("SELECT DISTINCT user_id FROM plans")
            return [row[0] for row in await cursor.fetchall()]


database = Database()
# asyncio.run(database.create_table())
