from aiogram.filters import Command, CommandStart
from aiogram import Router, types, F

from db import requests, messages
from config import *

router = Router()


@router.message(CommandStart())
async def start(message: types.Message):
    first_name = message.from_user.first_name
    await message.answer(f"""👋 Assalomu alaykum <b>{first_name}</b> botimizga xush kelibsiz.

Yordam uchun: /help komandasini bosing.""", parse_mode="HTML", reply_markup=menu_buttons.as_markup(resize_keyboard=True))


@router.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer(messages.help_msg, parse_mode="HTML", reply_markup=menu_buttons.as_markup(resize_keyboard=True))


@router.message(F.text == button_names['help'])
async def help_handler_text(message: types.Message):
    await message.answer(messages.help_msg, parse_mode="HTML", reply_markup=menu_buttons.as_markup(resize_keyboard=True))
    

@router.message(Command("myinfo"))
async def myinfo_handler(message: types.Message):
    user_data = await requests.get_user_data(message.chat.id)

    if user_data:
        fullname, region, district, school, roleID = user_data
        role = "O'qituvchi" if roleID == 1 else "O'quvchi"
        msg = messages.myinfo_msg(fullname, region, district, school, role)
        await message.answer(msg, parse_mode="HTML", reply_markup=menu_buttons.as_markup(resize_keyboard=True))
    
    else:
        message.answer("🚫 Kechirasiz, siz ro'yxatdan o'tmagansiz. Ro'yxatdan o'tish uchun /register komandasini bosing.", reply_markup=menu_buttons.as_markup(resize_keyboard=True))


@router.message(F.text == button_names['myinfo'])
async def myinfo_handler_text(message: types.Message):
    user_data = await requests.get_user_data(message.chat.id)

    if user_data:
        fullname, region, district, school, roleID = user_data
        role = "O'qituvchi" if roleID == 1 else "O'quvchi"
        msg = messages.myinfo_msg(fullname, region, district, school, role)
        await message.answer(msg, parse_mode="HTML", reply_markup=menu_buttons.as_markup(resize_keyboard=True))
    
    else:
        message.answer("🚫 Kechirasiz, siz ro'yxatdan o'tmagansiz. Ro'yxatdan o'tish uchun /register komandasini bosing.", reply_markup=menu_buttons.as_markup(resize_keyboard=True))