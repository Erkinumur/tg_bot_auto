import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
admins = [
    os.getenv('ADMIN_ID'),
]

ip = os.getenv("IP")

db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
host = 'localhost'

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}
