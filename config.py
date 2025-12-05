import os
from os import getenv

# ------------------------------------------------

API_ID = int(os.environ.get("API_ID", "24569721"))
API_HASH = os.environ.get("API_HASH", "b0081b01a3f015d9c76f5ed9e7b20271")

# ------------------------------------------------

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "")

# -----------------------------------------------

OWNER_ID = int(os.environ.get("OWNER_ID", "7803657513"))
SPECIAL_ID = int(os.environ.get("SPECIAL_ID", "7803657513"))
# ------------------------------------------------

# ------------------------------------------------
LOGGER_ID = int(os.environ.get("LOGGER_ID", ""))

OTHER_LOGS = int(os.environ.get("OTHER_LOGS", ""))

# ------------------------------------------------

MONGO_URL = os.environ.get("MONGO_URL", "")

# ------------------------------------------------
