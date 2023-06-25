from aiogram.types import FSInputFile
from configs.configs import MEDIA_PATH

def get_photo_obj(item: dict) -> object:
    photo_path: str = MEDIA_PATH+item['photo']
    photo = FSInputFile(photo_path)
    return photo




