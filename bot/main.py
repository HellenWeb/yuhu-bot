from aiogram import executor

from bot.app import create_app
from bot.handlers import register_handlers


app = create_app()
register_handlers(app.dispatcher, app.services)


async def on_shutdown(_):
    app.connection.close()


def main():
    executor.start_polling(
        app.dispatcher,
        skip_updates=True,
        on_shutdown=on_shutdown,
    )
