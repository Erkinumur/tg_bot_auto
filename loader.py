import logging
import logging.config

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import yaml
import config

# logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
#                     level=logging.INFO)
with open('log_config.yml', 'r') as f:
    log_conf = yaml.safe_load(f.read())
logging.config.dictConfig(log_conf)

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


