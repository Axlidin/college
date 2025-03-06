from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from keyboards.default.users import Contact, profession, choices
from states.registrations import Registr
from loader import dp, bot


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"<b>Assalomu alaykum ismingizni kiriting...</b>")
    await Registr.first_name.set()

@dp.message_handler(state=Registr.first_name)
async def set_first_name(message: types.Message, state: FSMContext):
    first_name = message.text
    await state.update_data(
        {
        'first_name': first_name,
    }
    )
    await message.answer(f"<b>Ajoyib, familiyangizni kiriting...</b>")
    await Registr.last_name.set()

@dp.message_handler(state=Registr.last_name)
async def set_last_name(message: types.Message, state: FSMContext):
    last_name = message.text
    await state.update_data(
        {
        'last_name': last_name,
    }
    )
    await message.answer(f"<b>Siz bilan bog'lanish uchun telefon raqamingizni yozing 901234567 yoki pastdagi tugmani bosing...</b>",
                         reply_markup=Contact)
    await Registr.phone_number.set()


@dp.message_handler(content_types='contact', state=Registr.phone_number)
async def process_phone1(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    await state.update_data(
        {"phone": phone}
    )
    await message.answer(f"<b>Qaysi maktabda o'qiysiz...</b>", reply_markup=types.ReplyKeyboardRemove())
    await Registr.school.set()

@dp.message_handler(state=Registr.phone_number)
async def phoneNumber(message: types.Message, state: FSMContext):
    phone = message.text
    if phone.isdigit() and len(phone) == 9:
        await state.update_data(
            {'phone': f"+998{phone}"}
        )
        await message.answer(f"<b>Qaysi maktabda o'qiysiz...</b>", reply_markup=types.ReplyKeyboardRemove())
        await Registr.school.set()
    else:
        await message.answer("<b>Telefon raqami kiritishda xatolik yuzberdi, iltimos qaytadan kiriting. "
                             "Raqam 9 ta raqamdan iborat bo'lishi kerak.</b>")

@dp.message_handler(state=Registr.school)
async def set_school(message: types.Message, state: FSMContext):
    school = message.text
    await state.update_data(
        {'school': school}
    )
    await message.answer("<b>Yashash manzilingizni to'liq kiriting...\n</b>"
                         "<i>Navoiy viloyati, Konimex tumani</i>")
    await Registr.address.set()

@dp.message_handler(state=Registr.address)
async def set_address(message: types.Message, state: FSMContext):
    address = message.text
    await state.update_data(
        {'address': address}
    )
    await message.answer("<b>Ta'lim yo'nalishingizni tanlang...</b>", reply_markup=profession)
    await Registr.profession.set()

@dp.message_handler(state=Registr.profession)
async def set_profession(message: types.Message, state: FSMContext):
    profession = message.text
    await state.update_data(
        {'profession': profession}
    )
    data = await state.get_data()
    await message.answer(f"<b>Sizning ma'lumotlaringiz:</b>\n"
                         f"<b>Ismingiz:</b> {data['first_name']}\n"
                         f"<b>Familiyangiz:</b> {data['last_name']}\n"
                         f"<b>Telefon raqamingiz:</b> {data['phone']}\n"
                         f"<b>Sizning manzilingiz:</b> {data['address']}\n"
                         f"<b>Ta'lim yo'nalishingiz:</b> {data['profession']}\n")
    await message.answer("<b>Ma'lumotlaringini tasdiqlash uchun yuboring xatoliklar bo'lmasa!\n"
                         "Siz bilan tez orada bog'lanamiz.</b>",
                         reply_markup=choices)
    await Registr.final_step.set()

@dp.message_handler(state=Registr.final_step)
async def final_step(message: types.Message, state: FSMContext):
    user_choice = message.text
    if user_choice == "✅ Tasdiqlash":
        data = await state.get_data()
        result = "<b>Yangi ro'yxatdan o'tgan o'quvchi:\n\n</b>"
        result += (f"<b>FIO:</b> {data['first_name'].upper()} {data['last_name'].upper()}\n"
                  f"<b>Telefon raqami:</b> {data['phone']}\n"
                  f"<b>Manzil:</b> {data['address']}\n"
                   f"<b>Ta'lim yo'nalishi:</b> {data['profession']}\n")
        await message.answer(f"<b>Sizning ma'lumotlaringiz Adminga yuborildi:</b>\n"
                             f"<b>Ismingiz:</b> {data['first_name']}\n"
                             f"<b>Familiyangiz:</b> {data['last_name']}\n"
                             f"<b>Telefon raqamingiz:</b> {data['phone']}\n"
                             f"<b>Sizning manzilingiz:</b> {data['address']}\n"
                             f"<b>Ta'lim yo'nalishingiz:</b> {data['profession']}\n")
        await bot.send_message(ADMINS[0], result)
    elif user_choice == "🔄 Qayta yozish":
        await message.answer(f"<b>Assalomu alaykum ismingizni kiriting...</b>")
        await Registr.first_name.set()
    elif user_choice == "❌ Bekor qilish":
        await message.answer("<b>Sizning ma'lumotlaringiz bekor qilindi.</b>")
        await state.finish()