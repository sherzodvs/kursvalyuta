import logging
import requests
from datetime import date
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '1978401646:AAHRLJYgd1-emuOsSzRvCeATIzl0zHg-jyM'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

buttons = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
button1 = KeyboardButton('Hozirgi valyuta kursini bilish')
buttons.add(button1)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    start  = f"Salom hurmatli {message.from_user.first_name} \nBotimizga Hush kelibsiz!!!\n\nValyuta kursini bilish uchun pastdagi knopkani bosing!!!👇"
    await message.reply(start, reply_markup=buttons)


@dp.message_handler()
async def echo(message: types.Message):
    if message.text == "Hozirgi valyuta kursini bilish":
        url = 'https://cbu.uz/uz/arkhiv-kursov-valyut/json/'
        r = requests.get(url)
        res = r.json()
        for response in res:
            if (response['Ccy'] == 'EUR'):
                eur = response['Rate']
                kun = response['Date']
            elif(response['Ccy'] =='USD'):
                usd = response['Rate']
            elif(response['Ccy'] =='RUB'):
                rub = response['Rate']
                break
        valyuta = f"Bugungi 🕤 {date.today()} dagi valyuta kursi\n\n1 💶 EVRO = {eur} so'm\n1 💵 AQSH dollari = {usd} so'm\n1 🇷🇺 Rossiya rubli = {rub} so'm\n\n♻Oxirgi yangilanish: {kun} ♻"
        await message.answer(valyuta)
    else:
        await message.answer("Valyuta kursini bilish uchun knopkani bosing!!!👇", reply_markup=buttons)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)