from aiogram.fsm.state import State, StatesGroup


class TestManage(StatesGroup):
    teacher_state = State()
    student_state = State()