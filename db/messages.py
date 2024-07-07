from datetime import datetime, timedelta
import pytz
from config import *


test_create_on_start = """1️⃣ Test yaratish uchun

+test*Fan nomi*to'g'ri javoblar

ko'rinishida yuboring.

Misol: 
+test*Informatika*abbccdd..."""

test_solve_on_start = """1️⃣ Testga yechim yuborish uchun

testID*to'g'ri javoblar

ko'rinishida yuboring. Masalan:

000123*abcdea...
"""


help_msg = """☝️ Mazkur bot testlar yechish maqsadida foydalaniladi. O'qituvchi test yaratadi, o'quvchi esa uni yechadi va natijasini bilib oladi. Quyida botda mavjud komandalar bilan tanishasiz:

<b>Umumiy</b>:
/start - Botni ishga tushirish
/myinfo - Shaxsiy ma'lumotlar
/help - Yordam


<b>O'qituvchi</b>:
/start - Test yaratish uchun umumiy shablon
/starttest - Yaratilgan testni boshlash
/finishtest - Testni tugatish

<b>O'quvchi</b>:
/start - test yechish uchun umumiy shablon
"""

def myinfo_msg(fullname, region, district, school, role):
    role_emoji = "🧑‍🏫" if role == 1 else "🧑‍🎓"
    role_str = "O'qituvchi" if role == 1 else "O'quvchi"
    timezone = pytz.timezone("Asia/Tashkent")
    curr_time = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')
    msg = f"""ℹ️ Sizning ma'lumotlaringiz:
------------------------------------------------------------
👤 Ism: <b>{fullname}</b>

📍 Hudud: <b>{region}</b>
📍 Tuman: <b>{district}</b>

🏫 Maktab: <b>{school}</b>
{role_emoji} Rol: <b>{role_str}</b>
-----------------------------------------------------------
Joriy vaqt: {curr_time}
    """


    return msg


def test_success_msg(testID: int, num_of_answers: int):
    msg = f"""✅ Testingiz muvaffaqiyatli yaratildi!

Test kodi: <b>{testID}</b>
Savollar soni: <b>{num_of_answers}</b>

Testda qatnashuvchilar quyidagi ko`rinishda javob yuborishlari mumkin:
{testID}*abcdea...

"""

    return msg



def student_report(fullname, school, testID, student_answers, score, score_p, submitted_at):
    report_msg = f"""👤 Foydalanuvchi: <b>{fullname}</b>
🏫 Maktab: <b>{school}</b>
📖 Test kodi: <b>{test_id_repr(testID)}</b>
✏️ Jami savollar soni: <b>{len(student_answers)} ta</b>
✅ To'g'ri javoblar soni: <b>{score} ta</b>
🔣 Foiz : <b>{score_p}</b> %

🕐 Topshirilgan vaqti: <b>{submitted_at}</b>
    """
    
    return report_msg