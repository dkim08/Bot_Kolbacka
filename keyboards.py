from aiogram import types

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1) # добавление кнопок
btn_wb = types.KeyboardButton(text='черно-белый') 
btn_rez = types.KeyboardButton(text='резкость')
btn_blur = types.KeyboardButton(text='размыть')
btn_back = types.KeyboardButton(text='назад')

keyboard.add(btn_wb, btn_rez, btn_blur, btn_back)

empty_keyboard = types.ReplyKeyboardRemove()