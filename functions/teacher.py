from datetime import datetime

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from states.test import TestCreation, TestManage
from config import *
from db import requests, messages


router = Router()


@router.message()
async def get_test(message: types.Message, state: FSMContext):
    test = message.text
    tst_list = test.split("*")
    if not test.startswith("+test") or len(tst_list) != 3:
        message.answer("🚫 Kechirasiz, siz test yaratish shabloniga amal qilmayapsiz. Iltimos boshidan kiriting:")
    else:
        subject = tst_list[1]
        answers = tst_list[2]
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        is_test_created = await requests.create_test_on_db(message.chat.id, subject, created_at, answers)

        if is_test_created:
            testID_repr = test_id_repr(is_test_created)
            num = len(answers)
            msg = messages.test_success_msg(testID_repr, num)
            await message.answer(msg, parse_mode="HTML")
            state.clear()
        else:
            await message.answer("Test yaratish jarayonida muammo yuzaga keldi. Iltimos, keyinroq urinib ko'ring.")
            state.clear()



@router.message(Command("finishtest"))
async def finish_test(message: types.Message, state: FSMContext):
    own_tests_markup = InlineKeyboardBuilder()
    all_ongoing_tests = await requests.get_all_ongoing_tests(message.chat.id)

    if all_ongoing_tests:
        for test in all_ongoing_tests:
            test_repr = test_id_repr(test)
            own_tests_markup.add(types.InlineKeyboardButton(text=test_repr, callback_data=f"ongoing_test:{test}"))
        own_tests_markup.adjust(2)

        await message.answer("Qaysi testni tugatmoqchisiz?", reply_markup=own_tests_markup.as_markup())
        await state.set_state(TestManage.waiting_for_test_id_to_finish)
    else:
        await message.answer("Kechirasiz, hozir sizda davom etayotgan test mavjud emas.")


@router.callback_query(TestManage.waiting_for_test_id_to_finish)
async def get_finish_test(call: types.CallbackQuery, state: FSMContext):
    test = call.data.split(":")[1]
    test_repr = test_id_repr(test)

    is_finished = await requests.finish_test(test)

    if is_finished:
        await call.message.edit_text(f"{test_repr}-test yakunlandi.")

        await requests.generate_test_report(call.message, test)
        await state.clear()
    else:
        await call.message.edit_text("Testni tugatishda muammo yuzaga keldi.")