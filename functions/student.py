from datetime import datetime

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from states.test import TestSolve
from config import *
from db import requests


router = Router()


@router.message(Command("solve"))
async def solve_test(message: types.Message, state: FSMContext):
    is_student = await requests.validate_teacher(message.chat.id)

    if is_student:
        await message.answer("Test IDsini 6 xonali son ko'rinishida kiriting, masalan <b>000123</b>:", parse_mode="HTML")
        await state.set_state(TestSolve.waiting_for_test_id_to_solve)
    else:
        await message.answer("Hurmatli foydalanuvchi, siz botda ro'yxatdan o'tmagansiz. Ro'yxatdan o'tish uchun /register komandasini bosing.")


@router.message(TestSolve.waiting_for_test_id_to_solve)
async def get_test_id(message: types.Message, state: FSMContext):
    testID = int(message.text)
    test_exists = await requests.validate_test_request(testID)
    is_participated_before = await requests.check_participation_status(message.chat.id, testID)

    if test_exists:
        if is_participated_before:
            await message.answer("Kechirasiz, testga faqat 1 marta qatnashish mumkin.")
        else:
            await state.update_data(testID=testID)
            await message.answer("Javoblaringizni kiriting, masalan <b>AABDC</b>:", parse_mode="HTML")
            await state.set_state(TestSolve.waiting_for_answers_solution)
    else:
        await message.answer("Bunday test mavjud emas. Iltimos yana tekshirib ko'ring va qaytadan /solve komandasini bosing.")


@router.message(TestSolve.waiting_for_answers_solution)
async def get_answer_solution(message: types.Message, state: FSMContext):
    answers = message.text.upper()
    await state.update_data(answers=answers)
    await message.answer(f"Javoblaringiz: <b>{answers}</b>.", parse_mode="HTML", reply_markup=verify_buttons.as_markup())
    await state.set_state(TestSolve.waiting_for_verify_solutions)


@router.callback_query(TestSolve.waiting_for_verify_solutions)
async def verify_solution(call: types.CallbackQuery, state: FSMContext):
    is_verified = 1 if call.data == "verify" else 0
    await call.message.edit_text(f"✅ Tasdiqlandi." if is_verified else "❌ Bekor qilindi.")

    data = await state.get_data()
    submitted_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    correct_answers = await requests.get_all_correct_answers(data['testID'])
    student_answers = data['answers']
    score = 0

    if len(correct_answers) == len(student_answers):
        for i in range(0, len(correct_answers)):
            if correct_answers[i] == student_answers[i]:
                score+=1
    
    if is_verified:
        if correct_answers:
            are_solutions_submitted = await requests.save_participation(call.message.chat.id, data['testID'], score, submitted_at)
            if are_solutions_submitted:
                await call.message.answer("Javoblaringiz qabul qilindi!")
                await state.clear()
            else:
                call.message.answer("Javoblarni tekshirishda muammo yuzaga keldi.")
                await state.clear()
    else:
        await call.message.answer("Yangi test yaratish uchun /create komandasini bosing.")
        await state.clear()