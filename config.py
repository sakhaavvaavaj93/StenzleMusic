from os import getenv

from dotenv import load_dotenv

load_dotenv()


API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")

BOT_TOKEN = getenv("BOT_TOKEN", None)
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "180000"))

OWNER_ID = int(getenv("OWNER_ID"))

PING_IMG = getenv("PING_IMG" , "https://telegra.ph/file/89fd3e2bf5aaaef0b1373.jpg")
START_IMG = getenv("START_IMG", "https://telegra.ph/file/fe24e1a62b4e14bf8f4eb.jpg")

SESSION = getenv("SESSION", None)

SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/KURUK_SHE_TRA")
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/VRINDAAAVANAM/5")

SUDO_USERS = list(map(int, getenv("SUDO_USERS", "7089056796 7044382449").split()))


FAILED = "https://te.legra.ph/file/4c896584b592593c00aa8.jpg"
