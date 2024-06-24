from aiogram.fsm.state import State, StatesGroup

class TestCreation(StatesGroup):
    subjectID = State()
    waiting_for_num_of_tests = State()