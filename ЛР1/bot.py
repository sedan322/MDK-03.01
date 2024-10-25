# Импорт необходимых модулей
from aiohttp import web
from plugins import web_server

import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
from datetime import datetime

from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL, CHANNEL_ID, PORT

# Основной класс бота, наследующийся от класса Client из библиотеки pyrogram
class Bot(Client):
    def __init__(self):
        # Инициализация с передачей параметров из конфигурации
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER  # Логгер для вывода сообщений о работе

    async def start(self):
        # Запуск бота
        await super().start()
        usr_bot_me = await self.get_me()  # Получение информации о боте
        self.uptime = datetime.now()  # Сохранение времени старта

        # Проверка канала подписки, если указан FORCE_SUB_CHANNEL
        if FORCE_SUB_CHANNEL:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link  # Получение ссылки-приглашения
                if not link:  # Если ссылки нет, создаем ее
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                self.invitelink = link
            except Exception as a:
                # Обработка ошибок, если не удалось создать ссылку-приглашение
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Не удалось экспортировать ссылку-приглашение для канала Force Sub.")
                self.LOGGER(__name__).warning(f"Проверьте значение FORCE_SUB_CHANNEL и убедитесь, что бот является администратором с правами на приглашение пользователей, текущее значение: {FORCE_SUB_CHANNEL}")
                self.LOGGER(__name__).info("\nБот остановлен. Поддержка: https://t.me/CodeXBotzSupport")
                sys.exit()  # Завершение работы бота в случае ошибки

        # Проверка доступа к каналу базы данных, указанному в CHANNEL_ID
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel  # Сохранение объекта канала базы данных
            test = await self.send_message(chat_id=db_channel.id, text="Тестовое сообщение")  # Тестовое сообщение
            await test.delete()  # Удаление тестового сообщения
        except Exception as e:
            # Обработка ошибок доступа к каналу базы данных
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"Убедитесь, что бот является администратором в канале базы данных и проверьте значение CHANNEL_ID, текущее значение: {CHANNEL_ID}")
            self.LOGGER(__name__).info("\nБот остановлен. Поддержка: https://t.me/CodeXBotzSupport")
            sys.exit()  # Завершение работы бота в случае ошибки

        # Установка режима парсинга текста как HTML
        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"Бот запущен!\n\nСоздано \nhttps://t.me/CodeXBotz")
        self.LOGGER(__name__).info(f""" \n\n       
░█████╗░░█████╗░██████╗░███████╗██╗░░██╗██████╗░░█████╗░████████╗███████╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝╚██╗██╔╝██╔══██╗██╔══██╗╚══██╔══╝╚════██║
██║░░╚═╝██║░░██║██║░░██║█████╗░░░╚███╔╝░██████╦╝██║░░██║░░░██║░░░░░███╔═╝
██║░░██╗██║░░██║██║░░██║██╔══╝░░░██╔██╗░██╔══██╗██║░░██║░░░██║░░░██╔══╝░░
╚█████╔╝╚█████╔╝██████╔╝███████╗██╔╝╚██╗██████╦╝╚█████╔╝░░░██║░░░███████╗
░╚════╝░░╚════╝░╚═════╝░╚══════╝╚═╝░░╚═╝╚═════╝░░╚════╝░░░░╚═╝░░░╚══════╝
                                          """)
        self.username = usr_bot_me.username  # Сохранение имени пользователя бота

        # Запуск веб-сервера для обработки HTTP-запросов
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"  # Привязка к адресу 0.0.0.0 для работы на всех интерфейсах
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        # Остановка бота
        await super().stop()
        self.LOGGER(__name__).info("Бот остановлен.")
