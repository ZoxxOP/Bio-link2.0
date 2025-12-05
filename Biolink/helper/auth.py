from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

mongo = MongoCli(MONGO_URL)
authdb = mongo.auth.authusers

# ADD AUTHORIZED USER
async def add_auth(chat_id: int, user_id: int):
    """Add a user to the authorized users list for a chat."""
    if await is_auth(chat_id, user_id):
        return
    await authdb.insert_one({"chat_id": chat_id, "user_id": user_id})

# REMOVE AUTHORIZED USER
async def remove_auth(chat_id: int, user_id: int):
    """Remove a user from the authorized users list for a chat."""
    if not await is_auth(chat_id, user_id):
        return
    await authdb.delete_one({"chat_id": chat_id, "user_id": user_id})

# CHECK AUTHORIZED USER
async def is_auth(chat_id: int, user_id: int) -> bool:
    """Check if a user is authorized in a chat."""
    return bool(await authdb.find_one({"chat_id": chat_id, "user_id": user_id}))

# GET AUTHORIZED USERS
async def get_auth_users(chat_id: int) -> dict:
    """Get a list of all authorized users in a chat."""
    auth_users = []
    async for user in authdb.find({"chat_id": chat_id}):
        auth_users.append(user["user_id"])
    return {"auth_users": auth_users}
