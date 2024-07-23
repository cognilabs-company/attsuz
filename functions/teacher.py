from datetime import datetime

from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from states.test import TestManage
from config import *
from db import requests, messages


router = Router()


@router.message(TestManage.teacher_state)
async def get_test(message: types.Message, state: FSMContext):
    try:
        is_teacher = await requests.validate_teacher(message.chat.id)
        if is_teacher == 1:
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
                    await state.set_state(TestManage.teacher_state)
                else:
                    await message.answer("Test yaratish jarayonida muammo yuzaga keldi. Iltimos, keyinroq urinib ko'ring.")
                    await state.set_state(TestManage.teacher_state)
        elif is_teacher == 2:
            await message.answer("Kechirasiz, siz o'quvchi sifatida ro'yxatdan o'tgansiz. Siz test yarata olmaysiz.")
        else:
            await message.answer("Hurmatli foydalanuvchi, siz botda ro'yxatdan o'tmagansiz. Ro'yxatdan o'tish uchun qaytadan /start komandasini bosing.")
    except Exception as e:
        await bot.send_message(LOGS_CHANNEL, f"Error in get_test(): {e}")


@router.callback_query()
async def test_status(callback: types.CallbackQuery):
    try:
        status = callback.data.split("_")
        if status[0] == "current":
            testID = int(status[1])
            # await requests.generate_test_report(callback.message, testID)
            await requests.generate_current(callback.message, testID)
        elif status[0] == "finish":
            testID = int(status[1])
            await requests.finish_test(testID)
            callback.message.answer(f"⌛️ {testID}-test yakunlandi!")
            await requests.generate_test_report(callback.message, testID)
            await callback.message.delete()
        else:
            callback.message.answer("Kechirasiz, bunday tugma mavjud emas. Qayerdan topib bosgansiz bilmadiku, bizda bunaqasi yo'q :))")
            return
    except Exception as e:
        await bot.send_message(LOGS_CHANNEL, f"Error in test_status(): {e}")


