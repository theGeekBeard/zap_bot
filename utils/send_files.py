from loader import bot


async def send_files(chat_id, files):
    for file in files:
        try:
            await bot.send_video(chat_id, file[0])
        except:
            try:
                await bot.send_photo(chat_id, file[0])
            except:
                try:
                    await bot.send_document(chat_id, file[0])
                except:
                    pass
