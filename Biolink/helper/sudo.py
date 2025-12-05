from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

mongo = MongoCli(MONGO_URL)
sudodb = mongo.sudo.sudousers  # 'sudo' database aur 'sudousers' collection

# ADD SUDO USER
async def add_sudo(user_id: int):
    """Add a user to sudoers."""
    if await is_sudo(user_id):
        return
    await sudodb.insert_one({"user_id": user_id})

# REMOVE SUDO USER
async def remove_sudo(user_id: int):
    """Remove a user from sudoers."""
    if not await is_sudo(user_id):
        return
    await sudodb.delete_one({"user_id": user_id})

# CHECK SUDO
async def is_sudo(user_id: int) -> bool:
    """Check if a user is in sudo list."""
    return bool(await sudodb.find_one({"user_id": user_id}))

# GET ALL SUDOERS (FIXED)
async def get_sudoers() -> list:
    """Get a list of all sudo users."""
    sudo_list = []
    async for user in sudodb.find({}):
        sudo_list.append(user["user_id"])
    return sudo_list  # FIX: just return the list, not a dict
