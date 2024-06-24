from aiogram.fsm.state import State, StatesGroup

class TestCreation(StatesGroup):
    waiting_for_subject = State()
    waiting_for_answers = State()
    waiting_for_verify = State()


class TestManage(StatesGroup):
    waiting_for_test_id_to_start = State()
    waiting_for_test_id_to_finish = State()