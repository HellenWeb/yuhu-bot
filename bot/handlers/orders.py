from aiogram.dispatcher.filters import Text


def register(dispatcher, services):
    views = services.views

    @dispatcher.message_handler(commands=["history"])
    async def history_command(message):
        await views.send_orders(message)

    @dispatcher.message_handler(Text(equals="Заказы 📦"), state=None)
    async def orders_button(message):
        await views.send_orders(message)
