import sqlite3 as sq
from configs.configs import DB_PATH

def get_text_filters_from_db():
    
    '''
    получаем списки всех брендов, имен товаров и категори для использования в фильтрах хендлера
    возвращает в следующем порядке: all_categories, all_names, all_brands
    '''
    with sq.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('''SELECT DISTINCT
                        brand 
                        FROM shopapp_item
        ''')
        all_brands: list = [item[0] for item in cur.fetchall()]
        

        cur.execute('''SELECT DISTINCT 
                    NAME
                    FROM SHOPAPP_CATEGORY
        ''')
        all_categories: list = [item[0] for item in cur.fetchall()]
        
        cur.execute('''SELECT DISTINCT
                        title 
                        FROM shopapp_item
        ''')

        all_names: list = [name[0] for name in cur.fetchall()]
    return all_categories, all_names, all_brands


def get_item(category: str, brand: str, name: str) -> dict:
    '''
    Функция делает запрос к БД
    Возвращает отобранный товар в виде словаря, где ключь - название поля
    '''
    with sq.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('''SELECT 
                        ITEM.TITLE, ITEM.SIZE, ITEM.PRICE, ITEM.BRAND, ITEM.COUNT, CAT.NAME AS category, MAX(PHOTO.PHOTO) AS photo
                        FROM shopapp_item ITEM
                        INNER JOIN SHOPAPP_CATEGORY CAT
                        ON ITEM.CATEG_ID = CAT.ID
                        LEFT JOIN (
                            SELECT *
                            FROM SHOPAPP_ITEMPHOTO
                        ) PHOTO
                        ON ITEM.ID = PHOTO.ITEM_ID
                        WHERE CAT.NAME = ? AND ITEM.BRAND = ? AND ITEM.TITLE = ?
        ''', (category, brand, name))
# 
#  GROUP BY ITEM_ID
# LIMIT 1
        
        fields = [title[0] for title in cur.description]
        items: list = [item for item in cur.fetchall()[0]]
    return dict(zip(fields, items))

def get_brands(category: str) -> list:
    '''
    Принимает название категории
    Подключается к базе данных, отфильтровывает все поля по выбранной категории
    Возвращает список уникальных брендов
    '''

    with sq.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('''SELECT DISTINCT
                        ITEM.BRAND
                        FROM shopapp_item ITEM
                        INNER JOIN SHOPAPP_CATEGORY CAT
                        ON ITEM.CATEG_ID = CAT.ID
                        WHERE CAT.NAME = ?
        ''', (category,))
        brands: list = [brand[0] for brand in cur.fetchall()]
    return brands


def get_item_list(category: str, brand: str) ->list[str]:
    '''
    Принимает в качестве фильтров категорию и бренд,
    Делает запрос в БД
    возвращает список товаров прошедших фильтр
    '''
    with sq.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('''SELECT DISTINCT
                        ITEM.TITLE
                        FROM shopapp_item ITEM
                        INNER JOIN SHOPAPP_CATEGORY CAT
                        ON ITEM.CATEG_ID = CAT.ID
                        WHERE CAT.NAME = ? AND ITEM.BRAND = ?
        ''', (category, brand))
        items: list = [item[0] for item in cur.fetchall()]
        return items
