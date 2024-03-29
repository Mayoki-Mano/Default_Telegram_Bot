
from bot import *

db_path = 'db/database.db'
dir_path = 'db'
token = "6359553241:AAF6e_0uNzW-QoOPNu01Zh1zBndJi2e8WN4"
bot = Bot(token, dir_path, db_path)
bot.infinity_polling()

