from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("IP")
DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")

support_ids = [
    910624775,
]
