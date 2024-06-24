from datetime import datetime

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states.test import TestCreation
from config import *
from db import requests


router = Router()


@router.message(Command("create"))
async def create_test(message: types.Message, state: FSMContext):
    await message.answer("Fanni kiriting, masalan <b>Matematika</b>:", parse_mode="HTML", reply_markup=None)
    await state.set_state(TestCreation.waiting_for_subject)


@router.message(TestCreation.waiting_for_subject)
async def get_subject(message: types.Message, state: FSMContext):
    subject = message.text.lower().capitalize()
    await state.update_data(subject=subject)
    await message.answer("Test javoblarini kiriting, masalan <b>AABDC</b>: ", parse_mode="HTML", reply_markup=None)
    await state.set_state(TestCreation.waiting_for_answers)


@router.message(TestCreation.waiting_for_answers)
async def get_answers(message: types.Message, state: FSMContext):
    answers = message.text.upper()
    await state.update_data(answers=answers)
    await message.answer(f"Javoblaringiz: <b>{answers}</b>.", parse_mode="HTML", reply_markup=verify_buttons.as_markup())
    await state.set_state(TestCreation.waiting_for_verify)


@router.callback_query(TestCreation.waiting_for_verify)
async def get_verification(call: types.CallbackQuery, state: FSMContext):
    is_verified = 1 if call.data == "verify" else 0
    data = await state.get_data()
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if is_verified:
        testID = await requests.create_test_on_db(call.message.chat.id, data['subject'], created_at)
        are_questions_created = await requests.create_questions(testID, data['answers'])

        if are_questions_created:
            await call.message.answer(f"Test muvaffaqiyatli yaratildi. Test IDsi: {testID}")
            state.clear()
        else:
            await call.message.answer(f"Test yaratish jarayonida muammo yuzaga keldi.")
            state.clear()
    else:
        await call.message.answer("Siz testni bekor qildingiz. Yangi yaratish uchun /create komandasini bosing.")
        state.clear()