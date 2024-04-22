import os
from dotenv import load_dotenv


# ======================================================================================================================


load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
ADMIN_ID_LIST = [int(admin) for admin in os.getenv("ADMIN_ID_LIST").split(',')]
