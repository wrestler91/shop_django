from aiogram.fsm.state import StatesGroup, State
from dataclasses import dataclass

@dataclass
class FsmFindItem(StatesGroup):
    category_state: State = State()
    brand_state: State = State()
    size_state: State = State()
    name_state: State = State()

@dataclass
class FsmContact(StatesGroup):
    contact_state: State = State()