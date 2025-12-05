from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

mongo = MongoCli(MONGO_URL)
db = mongo.chats.chatsdb  # Directly pointing to the collection

async def get_chats():
    chat_list = []
    async for chat in db.find({"chat": {"$lt": 0}}):
        chat_list.append(chat['chat'])
    return chat_list

async def get_chat(chat):
    chats = await get_chats()
    return chat in chats

async def add_chat(chat):
    if await get_chat(chat):
        return
    await db.insert_one({"chat": chat})

async def del_chat(chat):
    if not await get_chat(chat):
        return
    await db.delete_one({"chat": chat})
