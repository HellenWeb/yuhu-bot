from aiogram.dispatcher.filters import Text


def register(dispatcher, services):
    views = services.views

    @dispatcher.message_handler(commands=["start", "help"])
    async def start(message):
        await views.send_main_menu(message)

    @dispatcher.message_handler(Text(equals="Помощь ❓"), state=None)
    async def help_button(message):
        await views.send_help(message)

    @dispatcher.message_handler(Text(equals="🏠"), state=None)
    async def home_button(message):
        await views.send_main_menu(message)
