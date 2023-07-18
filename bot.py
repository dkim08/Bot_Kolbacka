import logging#подключаем библиотеку логирования
from aiogram import Bot, Dispatcher, executor, types    
import random
import webbrowser
from translate import Translator
from PIL import Image
from keyboards import keyboard
API_TOKEN = '6122261793:AAEwwCvhzVqHH4kn-7P4hidplrPey6RvthU'#мой айди

logging.basicConfig(level=logging.INFO)


bot = Bot(token=API_TOKEN)#указываем боту мой токен/айди
dp = Dispatcher(bot)#отвечает на любые действия в определенной сфере
secret_number = 0 
attemps = 0
is_translate = False

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):#реагирует на входящие сообщения и содержит в себе функцию ответа
    bot_menu = '''- открывать youtube(чтобы запустить напишите слово *ютуб*) 
                - поддерживать диалог по аниме
                - накидывает на фото фильтры(чтобы запустить напишите команду /photo)
                - играет в 'угадай число(чтобы запустить напишите слово *игра*)'
                - переводитт слова с русского на английский(чтобы запустить напишите слово *перевод*)'''.strip() #меню
    await message.reply('Привет!\n Меня зовут Колбаска!\Я умею.' + bot_menu)#отвечает сообщения после нажатия старт


@dp.message_handler(commands=['send_photo'])
async def photo(message: types.Message):
    await bot.send_message(message.chat.id, "Отправьте картинку.")
    
@dp.message_handler(content_types=['photo'])
async def photo(message: types.Message): 
    await message.photo[-1].download("photo.jpg", make_dirs=False)
    print('saved')
    await message.answer('Я получил от тебя картинку',reply_markup=keyboard)    
    print('sent')
    
@dp.message_handler()#реагирует на входящие сообщения и содержит в себе функцию ответа
async def echo(message: types.Message):
    global secret_number, attempts
    
    if message.text == 'черно-белый':
        image = Image.open('photo.jpg')
        grayscale = image.convert('L')
        im1 = grayscale.save('new_photo.jpg')
        with open('new_photo.jpg', 'rb') as f:
            photo = f.read()
        await bot.send_photo(message.from_user.id, photo) 

    if message.text.lower() == 'какие аниме ты знаешь?':
        await message.answer('Я знаю Наруто, Клинок рассекающий демонов, Хантер х Хантер, Атака Титанов, Мга, Токийский гуль')
        await message.answer('Какое твое любимое аниме?')
        
    elif message. text.lower() == 'что ты умеешь делать?':
        await message.answer('Если вам интересно, что я умею, напишите команду /help')

    elif message.text.lower() == 'читал ли ты мангу?':
        await message.answer('Нет, не читал. Я смотрю аниме. Можешь спросить какое мое любимое аниме')
        await message.answer('А ты читаешь мангу?')

    elif message.text.lower() == 'какое твое любимое аниме?':
        await message.answer('Мое любимое аниме это Клиноок рассекающий демонов')

    elif message.text.lower() == 'какая арка из аниме твоя любимая?':
        await message.answer('В крд моя любимая арка это Квартал красных фонарей')
    
    elif message.text.lower() == 'хочешь ли ты продолжение твоего любимого аниме?':
         await message.answer('Да, я очень жду продолжение!')

    elif message.text.lower() == 'какой персонаж тебе нравится больше всего?':
        await message.answer('какой персонаж тебе нравится больше всего?')
        await message.answer('Мне нравится Танджиро, а тебе какой нравится?')
            
    elif message.text.lower() == 'какого персонажа ты больше всего не любишь?':
       await message.answer('Мне не нравится Мудзан, а тебе?')

    if message.text =='перевод':
        is_translate = True
        await message.answer('Включен режим перевода. Чтобы выключить, напишите *off*')
        
    elif message.text == 'off':
        is_translate = False
        await message.answer('Режим перевода выключен')

    elif is_translate == True:
        trans = Translator(from_lang='russian', to_lang='english')
        text = str(message.text)
        result = trans.translate(text)
        await message.answer(result)

    elif message.text.lower() == 'ютуб':
        webbrowser.open_new_tab('https://www.youtube.com/')


    elif message.text.lower() == 'игра':
        secret_number = random.randint(1,5)
        attemps = 3

        await message.answer('Число загаданно.У вас есть три попытки отгадать число')
        await message.answer('Напишите число от 1 до 5')

    elif message.text in '12345':
        if secret_number == message.text:
            secret_number = random.randint(1,5)
            attemps = 3
            await message.answer('Молодец! Ты угадал')
    elif secret_number != message.text and attemps != 0:
        attemps -= 1
        await message.answer('Не угадал. Попробуй снова  у тебя осталось', attemps, 'попыток')
    elif attemps == 0:
        secret_number = random.randint(1,5)
        attemps = 3
        await message.answer('Попытки закончились.Перезапусти игру заново')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)