from aiogram.filters import Command, CommandStart
from aiogram import Router, types, F
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext

from db import requests, messages
from config import *
from states.registration import Registration
from states.test import TestCreation

router = Router()


@router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    first_name = message.from_user.first_name
    intro_photo_path = f"{prod_dir}assets/images/start_bot.jpg"
    intro_file = FSInputFile(intro_photo_path)
    
    is_user_registered = await requests.user_is_registered(message.chat.id)
    if is_user_registered:
        msg = messages.test_create_on_start
        await message.answer(msg)
        state.set_state(TestCreation.waiting_for_test)
    else:
        await bot.send_photo(message.chat.id, intro_file, caption=f"""👋 Assalomu alaykum <b>{first_name}</b> botimizga xush kelibsiz.

Yordam uchun: /help komandasini bosing.""", parse_mode="HTML", reply_markup=menu_buttons.as_markup(resize_keyboard=True))
        await message.answer("Ism familiyangizni kiriting, masalan <b>Alijon Valiyev</b>:", parse_mode="HTML", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(Registration.waiting_for_name)


@router.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer(messages.help_msg, parse_mode="HTML", reply_markup=menu_buttons.as_markup(resize_keyboard=True))


@router.message(F.text == button_names['help'])
async def help_handler_text(message: types.Message):
    await message.answer(messages.help_msg, parse_mode="HTML", reply_markup=menu_buttons.as_markup(resize_keyboard=True))
    

@router.message(Command("myinfo"))
async def myinfo_handler(message: types.Message):
    user_data = await requests.get_user_data(message=message, userID=message.chat.id)
    print(user_data)


@router.message(F.text == button_names['myinfo'])
async def myinfo_handler_text(message: types.Message):
    user_data = await requests.get_user_data(message=message, userID=message.chat.id)
    print(user_data)