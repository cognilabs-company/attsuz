from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, StateFilter

from db.models import AsyncSession, User
from states.registration import Registration
from config import *

router = Router()

@router.message(Command("register"))
async def register_start(message: types.Message, state: FSMContext):
    await message.answer("Ism familiyangizni kiriting, masalan <i>Alijon Valiyev</i>:", parse_mode="HTML")
    await state.set_state(Registration.waiting_for_name)


@router.message(Registration.waiting_for_name)
async def register_name(message: types.Message, state: FSMContext):
    choose_region_kb = types.InlineKeyboardMarkup()
    for region in regions:
        button = types.InlineKeyboardButton(text=region, callback_data="region:" + region)
        choose_region_kb.add(button)
    await state.update_data(name=message.text)
    await message.answer("Qaysi viloyatdansiz?", reply_markup=choose_region_kb)
    await state.set_state(Registration.waiting_for_region)


@router.message(Registration.waiting_for_region)
async def register_region(callback_query: types.CallbackQuery, state: FSMContext):
    region = callback_query.data
    await state.update_data(region=region)
    
    districts = regions.get(region)
    if districts:
        choose_district_kb = types.InlineKeyboardMarkup()
        for district in districts:
            button = types.InlineKeyboardButton(text=district, callback_data="district:" + district)
            choose_district_kb.add(button)
    
    await callback_query.message.answer("Tumaningizni tanlang:", reply_markup=choose_district_kb)
    await state.set_state(Registration.waiting_for_district)


@router.callback_query(Registration.waiting_for_district)
async def register_district(callback_query: types.CallbackQuery, state: FSMContext):
    district = callback_query.data
    await state.update_data(district=district)
    await callback_query.message.answer("Maktabingizni kiriting, masalan <b>5-maktab</b>:", parse_mode="HTML")
    await state.set_state(Registration.waiting_for_school)


@router.message(Registration.waiting_for_school)
async def register_school(message: types.Message, state: FSMContext):
    await state.update_data(school=message.text)
    
    data = await state.get_data()
    name = data['name']
    username = data['username']
    region = data['region']
    school = data['school']
    
    # Save user to database
    session = AsyncSession()
    user = User(name=name, username=username, region=region, school=school)
    session.add(user)
    session.commit()
    session.close()
    
    await message.answer("Siz muvaffaqiyatli ro'yxatdan o'tdingiz!")
    await state.clear()


@router.message(Command("otmenreg"), F.state.in_(Registration))
async def cancel_registration(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state in [
        Registration.waiting_for_name.state, 
        Registration.waiting_for_region.state, 
        Registration.waiting_for_district.state, 
        Registration.waiting_for_school.state]:
        await state.clear()
        await message.answer("🛑 Siz ro'yxatdan o'tish jarayonini to'xtatdingiz.", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("☝️ Siz hozir ro'yxatdan o'tish jarayonida emassiz. Iltimos to'g'ri komandani kiriting.")