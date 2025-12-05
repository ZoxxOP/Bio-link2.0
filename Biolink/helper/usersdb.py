from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

mongo = MongoCli(MONGO_URL)
db = mongo.users.users  # Direct reference to the 'users' collection

async def get_users():
    user_list = []
    async for user in db.find({"user": {"$gt": 0}}):
        user_list.append(user['user'])
    return user_list

async def get_user(user):
    users = await get_users()
    return user in users

async def add_user(user):
    if await get_user(user):
        return
    await db.insert_one({"user": user})

async def del_user(user):
    if not await get_user(user):
        return
    await db.delete_one({"user": user})
