from aiogram.utils import executor
from create_bot import dp


async def on_startup(_):
	print('Бот вышел в онлайн')

from handlers import client, admin, other 

admin.register_handlers_admin(dp)
client.register_handlers_client(dp)
other.register_handlers_other(dp)






	



	# await message.reply(message.text)
	# await bot.send_message(message.from_user.id, message.text)




executor.start_polling(dp, skip_updates=True, on_startup=on_startup)