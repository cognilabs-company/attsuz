from datetime import datetime

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from states.test import TestManage
from config import *
from db import requests
from db import messages
from certigen import generate_certificate


router = Router()


@router.message(TestManage.student_state)
async def solve_test(message: types.Message):
    try:
        is_student = await requests.validate_teacher(message.chat.id)

        if is_student:
            solution = message.text
            solution_list = solution.split("*")
            if len(solution_list) == 2 and solution_list[0].isnumeric():
                testID = int(solution_list[0])
                answers = solution_list[1]
                is_test_exists = await requests.validate_test_request(testID)
                is_participated_before = await requests.check_participation_status(message.chat.id, testID)
                is_test_ended = await requests.is_test_ended(testID)
                if is_test_exists and not is_test_ended:
                    if is_participated_before:
                        await message.answer("Kechirasiz, har bir testga faqat 1 marta qatnashish mumkin.")
                        return
                    correct_answers = await requests.get_all_correct_answers(testID)
                    score = 0
                    submitted_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    if len(correct_answers) == len(answers):
                        for i in range(0, len(correct_answers)):
                            if correct_answers[i] == answers[i]:
                                score+=1
                    else:
                        await message.answer("Kiritilgan javoblar soni savollar soniga to'g'ri kelmadi. Iltimos, yechimingizni boshidan yuboring.")
                        return
                    
                    are_solutions_submitted = await requests.save_participation(message.chat.id, testID, score, submitted_at)
                    if are_solutions_submitted:
                        await message.answer("Javoblaringiz qabul qilindi!")
                        teacher_data = await requests.get_teacher_data(testID)
                        teacher_id = teacher_data[1]
                        text = f'Foydalanuvchi <a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a> <b>{testID}</b>-testga yechim yubordi.'
                        test_status_buttons = InlineKeyboardBuilder()
                        test_status_buttons.add(types.InlineKeyboardButton(text="Joriy holat", callback_data=f"current_{testID}"), types.InlineKeyboardButton(text="Yakunlash", callback_data=f"finish_{testID}"))
                        test_status_buttons.adjust(2)
                        await bot.send_message(teacher_id, text, parse_mode="HTML", reply_markup=test_status_buttons.as_markup())
                    else:
                        await message.answer("Javoblarni saqlashda muammo yuzaga keldi.")

                    user_data = await requests.user_is_registered(message.chat.id)
                    fullname = user_data[0]
                    school = user_data[3]
                
                    score_p = str((score / len(answers)) * 100)[:5]
                    print(user_data)
                    await message.answer(messages.student_report(fullname, school, testID, answers, score, score_p, submitted_at), parse_mode="HTML")
                    await generate_certificate(message.chat.id, testID)
                else:
                    await message.answer("Bunday test mavjud emas yoki allaqachon yakunlangan.")

            else:
                await message.answer("Iltimos, javoblarni to'g'ri formatda kiriting.")
        else:
            await message.answer("Hurmatli foydalanuvchi, siz botda ro'yxatdan o'tmagansiz. Ro'yxatdan o'tish uchun qaytadan /start komandasini bosing.")
    except Exception as e:
        await bot.send_message(LOGS_CHANNEL, f"Error in solve_test(): {e}")
