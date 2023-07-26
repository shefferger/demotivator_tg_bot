from telebot import async_telebot
import signal
import os
import asyncio


class App:
    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_handler)
        signal.signal(signal.SIGTERM, self.exit_handler)
        if not os.getenv('TOKEN'):
            print('Token not presented, exiting')
            return
        self.bot = async_telebot.AsyncTeleBot(os.getenv('TOKEN'))
        self.register_handlers()
        print('Bot started')
        asyncio.run(self.bot.polling())

    @staticmethod
    def exit_handler(signum, frame):
        print('exiting')
        for task in asyncio.tasks.all_tasks():
            task.cancel()

    def register_handlers(self):
        @self.bot.message_handler(commands=['help', 'start', 'status'])
        async def start_menu_handler(msg):
            cid = msg.chat.id
            await self.bot.send_message(chat_id=cid, text='Text', parse_mode='HTML')

        @self.bot.message_handler(content_types=['photo', 'document'])
        async def photo_handler(msg):
            if msg.content_type == 'photo' and msg.caption is not None:
                print('its photo with', msg.aption)
            elif msg.content_type == 'document' and msg.caption is not None:
                if msg.document.mime_type in ('image/png', 'image/pjpeg', 'image/jpeg', 'image/gif'):
                    print(f'its a doc {msg.document.mime_type} with', msg.caption)
            print(msg)
            cid = msg.chat.id
            await self.bot.reply_to(message=msg, text=msg.text)


if __name__ == '__main__':
    app = App()
