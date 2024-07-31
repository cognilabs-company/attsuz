import os

from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from dotenv import load_dotenv
from aiogram import Bot

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

BOT_TOKEN = os.getenv("BOT_TOKEN")
LOGS_CHANNEL = os.getenv("LOGS_CHANNEL")
SUBS_CHANNEL_1 = os.getenv("SUBS_CHANNEL_1")
SUBS_CHANNEL_2 = os.getenv("SUBS_CHANNEL_2")

SUBS_LINK_1 = "https://t.me/milliymathonline"
SUBS_LINK_2 = "https://t.me/Prezident_maktablari_uzz"


roles = ["O'qituvchi", "O'quvchi"]
regions = {
    "Toshkent shahri": ["Olmazor tumani", "Shayxontohur tumani", "Uchtepa tumani", "Chilonzor tumani", "Yunusobod tumani", "Mirobod tumani", "Yashnobod tumani", "Yakkasaroy tumani", "Sergeli tumani", "Bektemir tumani", "Yangihayot tumani", "Mirzo Ulug'bek tumani"],
    "Toshkent viloyati": ["Bekobod shahri","Bekobod tumani", "Bo'ka tumani", "Bo'stonliq tumani", "Chinoz tumani", "Ohangaron tumani", "Oqqo'rg'on tumani", "O'rta Chirchiq tumani", "Parkent tumani", "Piskent tumani", "Qibray tumani", "Quyi Chirchiq tumani", "Toshkent tumani", "Yangiyo'l tumani", "Yuqori Chirchiq tumani", "Zangiota tumani"],
    "Andijon viloyati": ["Ulug'nor tumani", "Baliqchi tumani", "Bo'ston tumani", "Shahrixon tumani", "Oltinko'l tumani", "Asaka tumani", "Marhamat tumani", "Buloqboshi tumani", "Andijon tumani", "Xo'jaobod tumani", "Jalaquduq tumani", "Qo'rg'ontepa tumani", "Xonobod tumani", "Andijon shahri"],
    "Namangan viloyati": ["Namangan tumani", "Mingbuloq tumani", "Kosonsoy tumani", "Pop tumani", "To'raqo'rg'on tumani", "Uychi tumani", "Chortoq tumani", "Yangiqo'rg'on tumani", "Norin tumani", "Uchqo'rg'on tumani", "Chust tumani", "Namangan shahri tumani", "Namangan shahri"],
    "Farg'ona viloyati": ["Oltiariq tumani", "Bag'dod tumani", "Beshariq tumani", "Buvayda tumani", "Dang'ara tumani", "Farg'ona tumani", "Furqat tumani", "Qo'shtepa tumani", "Quva tumani", "Rishton tumani", "So'x tumani", "Toshloq tumani", "Uchko'prik tumani", "O'zbekiston tumani", "Yozyovon tumani", "Farg'ona shahri"],
    "Sirdaryo viloyati": ["Oqoltin tumani", "Boyovut tumani", "Guliston tumani", "Xovos tumani", "Mirzaobod tumani", "Sayxunobod tumani", "Sardoba tumani", "Sirdaryo tumani", "Yangiyer tumani", "Shirin tumani", "Guliston shahri"],
    "Jizzax viloyati": ["Arnasoy tumani", "Baxmal tumani", "Do'stlik tumani", "Forish tumani", "G'allaorol tumani", "Sharof Rashidov tumani", "Mirzacho'l tumani", "Paxtakor tumani", "Yangiobod tumani", "Zomin tumani", "Zafarobod tumani", "Zarbdor tumani", "Jizzax shahri"],
    "Samarqand viloyati": ["Bulung'ur tumani", "Ishtixon tumani", "Jomboy tumani", "Kattaqo'rg'on tumani", "Qo'shrabot tumani", "Narpay tumani", "Nurobod tumani", "Oqdaryo tumani", "Paxtachi tumani", "Payariq tumani", "Pastdarg'om tumani", "Samarqand tumani", "Toyloq tumani", "Urgut tumani", "Samarqand shahri"],
    "Qashqadaryo viloyati": ["Chiroqchi", "Dehqonobod", "G'uzor", "Qamashi", "Qarshi", "Koson", "Kasbi", "Kitob", "Mirishkor", "Muborak", "Nishon", "Shahrisabz", "Yakkabog'", "Ko'kdala", "Qarshi shahri"],
    "Surxondaryo viloyati": ["Angor tumani", "Boysun tumani", "Denov tumani", "Jarqo'rg'on tumani", "Qiziriq tumani", "Qumqo'rg'on tumani", "Muzrabot tumani", "Oltinsoy tumani", "Sariosiyo tumani", "Sherobod tumani", "Sho'rchi tumani", "Termiz tumani", "Uzun tumani", "Termiz shahri"],
    "Navoiy viloyati": ["Konimex tumani", "Karmana tumani", "Qiziltepa tumani", "Xatirchi tumani", "Navbahor tumani", "Nurota tumani", "Tomdi tumani", "Uchquduq tumani", "Navoiy shahri"],
    "Buxoro viloyati": ["Olot tumani", "Buxoro tumani", "G'ijduvon tumani", "Jondor tumani", "Kogon tumani", "Qorako'l tumani", "Qorovulbozor tumani", "Peshku tumani", "Romitan tumani", "Shofirkon tumani", "Vobkent tumani", "Buxoro shahri"],
    "Xorazm viloyati": ["Bog'ot tumani", "Gurlan tumani", "Xonqa tumani", "Hazorasp tumani", "Xiva tumani", "Qo'shko'pir tumani", "Shovot tumani", "Urganch tumani", "Yangiariq tumani", "Yangibozor tumani", "Tuproqqal'a tumani", "Urganch shahri"],
    "Qoraqalpog'iston Respublikasi": ["Amudaryo tumani", "Beruniy tumani", "Chimboy tumani", "Ellikqal'a tumani", "Kegeyli tumani", "Mo'ynoq tumani", "Nukus tumani", "Qanliko'l tumani", "Qo'ng'irot tumani", "Qorao'zak tumani", "Shumanay tumani", "Taxtako'pir tumani", "To'rtko'l tumani", "Xo'jayli tumani", "Taxiatosh tumani", "Bo'zatov tumani", "Nukus shahri"]
}


button_names = {
    "myinfo": "👤 Mening ma'lumotlarim",
    "help": "🆘 Yordam",
}


menu_buttons = ReplyKeyboardBuilder()
menu_buttons.add(*[types.KeyboardButton(text=txt) for txt in list(button_names.values())])
menu_buttons.adjust(3)


bot = Bot(token=BOT_TOKEN)

def test_id_repr(testID):
    # This method converts integer test ID to string representation: 12 -> 000012
    return "0"*(6-len(str(testID)))+str(testID)

def format_simple_table(data):
    table = "<b>Joriy holat:</b>\n\n"
    for row in data:
        table += f"{row['O`rin']}. {row['Ism-familiya']} - {row['Natija']} - {row['Foiz']}%\n"
    return table

# prod_dir = ""
prod_dir = "/home/tuya/attsuz/"


async def check_subscription(userID):
    try:
        member1 = await bot.get_chat_member(chat_id=SUBS_CHANNEL_1, user_id=userID)
        member2 = await bot.get_chat_member(chat_id=SUBS_CHANNEL_2, user_id=userID)
        print(member1, member2)
        return member1.status in ['member', 'administrator', 'creator'] and member2.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(e)
        return False
    
subs_buttons = InlineKeyboardBuilder()
subs1 = types.InlineKeyboardButton(text="1-kanal", url=f"{SUBS_LINK_1}")
subs2 = types.InlineKeyboardButton(text="2-kanal", url=f"{SUBS_LINK_2}")
subs_buttons.add(subs1, subs2)