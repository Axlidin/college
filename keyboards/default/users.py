from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

###contact
Contact = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Telefon raqamini ulashing", request_contact=True),]
    ], resize_keyboard=True, one_time_keyboard=True
)

###profession
profession = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='⚡ Elektr jihozlariga xizmat ko‘rsatish va ta’mirlash'),
            KeyboardButton(text='💻 Axborot vositalari mashinalari va kompyuter tarmoqlar')
        ],
        [
            KeyboardButton(text='🚗 Avtomobillarni taʼmirlash va ularga xizmat koʻrsatish'),
            KeyboardButton(text='🚜 Traktorchi-mashinist')
        ]],
    resize_keyboard=True,
    one_time_keyboard=True
)

#choice\
choices = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✅ Tasdiqlash"),
            KeyboardButton(text="🔄 Qayta yozish")
        ],
        [
            KeyboardButton(text="❌ Bekor qilish"),
        ]],
    resize_keyboard=True,
    one_time_keyboard=True
)