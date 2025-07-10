async def scheduled_parse():
    print("Запущен scheduled_parse")  # Отладочное сообщение
    async for text, source in parse_channels():
        print(f"Найдена новость: {text[:50]}...")  # Вывод первых 50 символов
        await post_to_channel(text, source)