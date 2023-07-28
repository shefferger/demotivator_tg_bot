import uuid

from telebot import async_telebot
import signal
import os
import asyncio
import image


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
        @self.bot.message_handler(commands=['help', 'start'])
        async def start_menu_handler(msg):
            cid = msg.chat.id
            text = 'Привет!\nДля создания демотиватора пришли фотографию с ' \
                   'текстом одним сообщением.\n\nИзображение должно быть не меньше 100x100px и не больше 10MB. Текст ' \
                   'должен быть не больше 200 символов. Принимаются изображения формата png, jpeg, gif. Если картинке ' \
                   'необходимо кадрирование - воспользуйся встроенным в телеграм редактором.'
            await self.bot.send_message(chat_id=cid, text=text, parse_mode='HTML')

        @self.bot.message_handler(content_types=['photo', 'document'])
        async def photo_handler(msg):
            if msg.caption is None:
                await self.bot.reply_to(message=msg, text='Вы не написали текст, попробуйте еще раз')
                return
            elif len(msg.caption) > 200:
                await self.bot.reply_to(message=msg, text='Вы указали слишком длинный текст (не больше 200 символов)')
                return
            file_id, img_result = None, None
            if msg.content_type == 'photo' and msg.caption is not None:
                file_id = msg.photo[-1].file_id
            elif msg.content_type == 'document' and msg.caption is not None:
                if msg.document.mime_type in ('image/png', 'image/pjpeg', 'image/jpeg', 'image/gif'):
                    file_id = msg.document.file_id
            cid = msg.chat.id
            print(f'cid: {cid}, text: {msg.caption}')
            if file_id:
                file_info = await self.bot.get_file(file_id)
                img = await self.bot.download_file(file_info.file_path)
                img_result = image.make_demotivator(img=img, text=msg.caption)
            if img_result:
                await self.bot.send_photo(chat_id=cid, photo=img_result)
            else:
                await self.bot.reply_to(message=msg, text='Произошла ошибка')


if __name__ == '__main__':
    app = App()
