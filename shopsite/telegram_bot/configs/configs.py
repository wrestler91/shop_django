from dataclasses import dataclass
from environs import Env


MEDIA_PATH = 'C:/Users/Арутюн/Desktop/python/проекты/магазин_на_джанго/shop/shopsite/media/'
DB_PATH = 'C:/Users/Арутюн/Desktop/python/проекты/магазин_на_джанго/shop/shopsite/db.sqlite3'
SITE_URL = 'https://www.google.com'
@dataclass
class TgBot:
    token: str


@dataclass
class Configs:
    tg_bot: TgBot


def load_configs(path: str = None) -> Configs:
    env = Env()
    env.read_env(path)
    return Configs(tg_bot=TgBot(token=env('BOT_TOKEN')))