from aiogram.dispatcher.filters import Text


def register(dispatcher, services):
    views = services.views

    @dispatcher.message_handler(commands=["about"])
    async def about_command(message):
        await views.send_about(message)

    @dispatcher.message_handler(Text(equals="О нас ❕"), state=None)
    async def about_button(message):
        await views.send_about(message)
