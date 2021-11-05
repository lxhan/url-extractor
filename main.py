from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import os
from aiogram import Bot, Dispatcher, executor, types, utils


API_VIDEO_URL = os.environ.get("API_VIDEO_URL")
TG_API_TOKEN = os.environ.get("TG_API_TOKEN")

bot = Bot(token=TG_API_TOKEN)
dp = Dispatcher(bot)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)


@dp.message_handler(commands=["start"])
async def send_welcome(message):
    await message.reply("Отправь мне ссылку с видео")


@dp.message_handler()
async def ask_for_url(message: types.Message):
    try:
        await message.reply("Дай мне немного времени")
        input_url = message.text
        driver.get(input_url)
        video_url = ""
        pk = ""
        for request in driver.requests:
            if request.response and API_VIDEO_URL in request.url:
                video_url = request.url
                pk = request.headers.get("accept")
        if video_url:
            headers = {
                "accept": pk
            }
            r = requests.get(url=video_url, headers=headers)
            data = r.json()
            sources = data["sources"]
            src_url = sources[-1]["src"]
            await message.answer(utils.markdown.link(title="Вот держи видео", url=src_url), parse_mode="MarkdownV2")
    except Exception as e:
        await message.answer("Что то не так с сылкой ¯\_(ツ)_/¯")
        return


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
