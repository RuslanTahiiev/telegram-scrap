import asyncio
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hunderline, hlink
from aiogram.dispatcher.filters import Text
from config import TOKEN, user_id
from main import update_news, get_first_news

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    my_buttons = ['Все новости', 'Последняя новость', 'Обновить']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*my_buttons)
    await message.answer(f'{hunderline("Лента новостей")}', reply_markup=keyboard)


#@dp.message_handler(commands='all_news')
@dp.message_handler(Text(equals='Все новости'))
async def get_news(message: types.Message):
    #get_first_news()
    with open('news.json', 'r', encoding='utf-8') as file:
        news = json.load(file)

    for k, w in sorted(news.items()):
        url = w['article_url']
        title = w['article_title']
        """article = f"<b>{w['article_date']}</b>\n" \
                  f"<u>{w['article_title']}</u>\n" \
                  f'<a href="{url}">{title}</a>'"""
        """article = f'{hbold(w["article_date"])}\n' \
                  f'{hunderline(w["article_title"])}\n' \
                  f'{hlink(title, url)}'"""
        article = f'{hbold(w["article_date"])}\n' \
                  f'{hlink(title, url)}'
        await message.answer(article)


#@dp.message_handler(commands='new_article')
@dp.message_handler(Text(equals='Последняя новость'))
async def get_new_article(message: types.Message):
    with open('news.json', 'r', encoding='utf-8') as file:
        news = json.load(file)

    for k, w in sorted(news.items())[-1:]:
        url = w['article_url']
        title = w['article_title']
        article = f'{hbold(w["article_date"])}\n' \
                  f'{hlink(title, url)}'
        await message.answer(article)


#@dp.message_handler(commands='refresh')
@dp.message_handler(Text(equals='Обновить'))
async def check_update_news(message: types.Message):
    refresh = update_news()
    if refresh:
        for k, w in sorted(refresh.items()):
            url = w['article_url']
            title = w['article_title']
            article = f'{hbold(w["article_date"])}\n' \
                      f'{hlink(title, url)}'
            await message.answer(article)
    else:
        await message.answer(f'{hbold("Нет ничего нового...")}')


async def news_sender():
    while True:
        refresh = update_news()
        if refresh:
            for k, w in sorted(refresh.items()):
                url = w['article_url']
                title = w['article_title']
                article = f'{hbold(w["article_date"])}\n' \
                          f'{hlink(title, url)}'

                await bot.send_message(user_id, article)
        else:
            await bot.send_message(user_id, f'{hbold("Нет ничего нового...")}', disable_notification=True)

        await asyncio.sleep(20)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(news_sender())
    executor.start_polling(dp)
