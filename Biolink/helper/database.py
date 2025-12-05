import datetime
from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

mongo = MongoCli(MONGO_URL)

users_collection = mongo.users.users
chats_collection = mongo.chats.chatsdb

# USERS FUNCTIONS
async def get_users():
    user_list = []
    async for user in users_collection.find({"user": {"$gt": 0}}):
        user_list.append(user['user'])
    return {"users": user_list}

async def get_user(user):
    data = await get_users()
    return user in data["users"]

async def add_user(user):
    if await get_user(user):
        return
    await users_collection.insert_one({
        "user": user,
        "joined_at": datetime.datetime.utcnow()
    })

async def del_user(user):
    if not await get_user(user):
        return
    await users_collection.delete_one({"user": user})

async def get_new_users():
    one_day_ago = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    return await users_collection.count_documents({"joined_at": {"$gte": one_day_ago}})

# CHATS FUNCTIONS
async def get_chats():
    chat_list = []
    async for chat in chats_collection.find({"chat": {"$lt": 0}}):
        chat_list.append(chat['chat'])
    return {"chats": chat_list}

async def get_chat(chat):
    data = await get_chats()
    return chat in data["chats"]

async def add_chat(chat):
    if await get_chat(chat):
        return
    await chats_collection.insert_one({
        "chat": chat,
        "joined_at": datetime.datetime.utcnow()
    })

async def del_chat(chat):
    if not await get_chat(chat):
        return
    await chats_collection.delete_one({"chat": chat})

async def get_new_chats():
    one_day_ago = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    return await chats_collection.count_documents({"joined_at": {"$gte": one_day_ago}})
