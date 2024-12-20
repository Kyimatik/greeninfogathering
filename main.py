import json
import asyncio
import logging
import sys
import os 

 
from aiogram import Bot, Dispatcher, Router, types , F 
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart , Command
from aiogram.types import Message , CallbackQuery ,FSInputFile
from aiogram.types import ReplyKeyboardMarkup , InlineKeyboardMarkup , InlineKeyboardButton ,ReplyKeyboardRemove 
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup , State
import pytz 
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from datetime import datetime


USER_FILE = r"test.txt"

# Создание списка пользователей
def load_users():
    """Загружает пользователей построчно из файла."""
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r', encoding='utf-8') as file:
            return file.readlines()  # Считываем строки в список
    return []  # Если файла нет, возвращаем пустой список


def save_user(user_id):
    with open(USER_FILE, 'a') as file:
        file.write(f"{user_id}\n")









# TOKEN = "?"
TOKEN = "?"

bot = Bot(TOKEN)
dp = Dispatcher()
router = Router()

presentation = "BQACAgQAAxkBAAMVZ2K9-ziBzbYQ0vBAARuneY3e-sIAAsEUAAJbrxhTBuOzVoADs-Y2BA" # Презентация 

# Кнопочка , для наших пользователей 
vseverno = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="""Получить приглашение 🎁""",url="https://t.me/green24official_bot?start")
        ]
    ],
    resize_keyboard=True
)

yesiwant = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="""Да я хочу учавствовать 🤩""",callback_data="YES")
        ]
    ],
    resize_keyboard=True
)

class Form(StatesGroup):
    form = State()

# Команда для создания текста с кнопкой 
@dp.message(F.text.lower() == "а")
async def getstarted(message: Message):
    await message.answer("""Приветствую! 🎉 20 декабря состоится уникальное мероприятие для байеров от компании Green Brand. Мы приготовили:
 • Экскурсию по нашему цеху и головному офису,
 • Разбор болей байеров и селлеров,
 • Практические советы для роста вашего бизнеса.
 • Избежать ошибок при закупках,
 • Найти новые возможности для роста,
 • Увидеть, как работают лучшие в своем деле.
 • Какие системные ошибки мешают байерам экономить,
 • Как выстроить партнерство с селлерами,
 • И покажем наш процесс изнутри.

Хотите узнать больше? Нажми на кнопку ниже
""",reply_markup=vseverno,parse_mode="HTML")



@dp.message(Command("start"))
async def getstarted(message: Message):
    usid = str(message.from_user.id)
    users = load_users()
    if usid not in users:
        save_user(usid)
        print("Вы успешно зарегистрированы")
    await message.answer_document(presentation)
    await message.answer("""Спасибо за ваш интерес к нашему мероприятию!

В приложении вы найдете презентацию, где подробно рассказано о программе события, месте проведения и ключевых моментах.

Просмотрите материал и оставьте заявку, чтобы присоединиться к нам 20 декабря. Мы будем рады видеть вас!

С уважением, команда <b>Green Brand</b>. 🤗""",reply_markup=yesiwant,parse_mode="HTML")




@dp.callback_query(lambda callback_query: callback_query.data == "YES")
async def pricecount(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("<b>Напишите ваше имя - номер</b>\n<i>Пример:Азамат - 0782444555</i>",parse_mode="HTML")
    await state.set_state(Form.form)

@dp.message(Form.form)
async def savetotxtfile(message: Message,state: FSMContext):
    user_text = message.text
    # Проверяем, существует ли файл, если нет, создаем его
    file_path = 'greenevent.txt'
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            pass  # Создаем пустой файл, если его нет
    
    # Сохраняем текст в файл
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(f'{user_text}\n')  # записываем текст в файл, каждое новое сообщение на новой строке
    await state.clear()
    await message.answer("Ваша заявка принята! Спасибо за внимание.")









@dp.message(F.content_type.in_({'document'}))
async def getid(message: Message):
    await message.answer(message.document.file_id)


# Функция для обработки файла и получения уникальных ID
def get_unique_user_ids(filename):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
        # Добавляем в set, чтобы убрать дубликаты
        unique_ids = set(line.strip() for line in lines if line.strip().isdigit())
    return unique_ids


# Функция для отправки сообщений
async def send_messages_to_users():
    text = """
<b>Внимание, друзья!</b>

Сегодня, <b>20 декабря</b>, пройдет наш долгожданный ивент «Тур для Байеров» от компании Green, который вы точно не захотите пропустить! Если вы уже зарегистрировались, ваше имя в списке, и мы с нетерпением ждем встречи с вами.

Но у нас есть две важные просьбы:

<b>1️⃣ Заполните короткую анкету</b> — это займет всего пару минут, но ваша обратная связь для нас бесценна.
👉 Пройти опрос (https://forms.gle/xgNipWG3cF657NoA6)

<b>2️⃣ Если вы еще не успели подтвердить участие на ивент «Тур для Байеров»</b>, подтвердите свой приход до 11:00 по ссылке:
👉 Подтвердить участие (https://t.me/green24official_bot?start)

Это поможет нам подготовиться и сделать мероприятие еще лучше для вас!

Спасибо за вашу активность! До встречи на ивенте!
"""
    user_ids = get_unique_user_ids("test.txt")
    print(user_ids)
    for user_id in user_ids:
        try:
            await bot.send_message(chat_id=int(user_id), text=f"{text}",parse_mode="HTML")
            print(f"Сообщение отправлено пользователю {user_id}")
        except Exception as e:
            print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")


@dp.message(F.text.lower() == "файл")
async def getfile(message: Message):
    all_media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Green Mail')
    # txtfile = FSInputFile(path=os.path.join(all_media_dir, 'users.txt'))
    txtfile = FSInputFile(r"C:\Users\echoe\OneDrive\Documents\Green Mail\greenevent.txt")
    await message.answer_document(document=txtfile) # отправка самого сообщения 


@dp.message(Command("san"))
async def getsan(message : Message):
    text = """
<b>Внимание, друзья!</b>

Сегодня, <b>20 декабря</b>, пройдет наш долгожданный ивент «Тур для Байеров» от компании Green, который вы точно не захотите пропустить! Если вы уже зарегистрировались, ваше имя в списке, и мы с нетерпением ждем встречи с вами.

Но у нас есть две важные просьбы:

<b>1️⃣ Заполните короткую анкету</b> — это займет всего пару минут, но ваша обратная связь для нас бесценна.
👉 Пройти опрос (https://forms.gle/xgNipWG3cF657NoA6)

<b>2️⃣ Если вы еще не успели подтвердить участие на ивент «Тур для Байеров»</b>, подтвердите свой приход до 11:00 по ссылке:
👉 Подтвердить участие (https://t.me/green24official_bot?start)

Это поможет нам подготовиться и сделать мероприятие еще лучше для вас!

Спасибо за вашу активность! До встречи на ивенте!
"""
    await bot.send_message(7388391479,text,parse_mode="HTML")




async def main() -> None:
    scheduler = AsyncIOScheduler(timezone="Asia/Bishkek")  # Устанавливаем часовой пояс
    # Настраиваем задачу на выполнение 20 декабря в 9:00
    send_time = datetime(2024, 12, 19, 18, 7)  # Год, месяц, день, час, минута
    scheduler.add_job(send_messages_to_users,trigger="date", run_date=send_time)

    
    # Добавляем задачу на 20:04 с понедельника по пятницу
    
    # Запускаем планировщик в фоновом режиме
    scheduler.start()
    
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    
    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())