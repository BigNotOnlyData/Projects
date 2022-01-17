from aiogram import types

from loader import dp
from utils.intent import get_intent_answer
from utils.toxic import get_probabality_toxic


@dp.message_handler()
async def intentANDtoxic(message: types.Message):
    """
    Возвращает интент и токсичность текста, если они были вычислены
    :param message:
    :return:
    """
    intent = get_intent_answer(message.text)
    toxic = get_probabality_toxic(message.text)
    toxic_text = '<code>Вероятность токсичности:</code><b>{toxic:.2f}</b>\nПожалуйста, будте вежливы🙏'
    if intent and toxic:
        me = await dp.bot.get_me()
        answer = toxic_text + '\n\n' + '{name}: {intent}'
        await message.reply(answer.format(toxic=toxic, name=me.first_name, intent=intent))
    elif intent:
        await message.reply(intent)
    elif toxic:
        await message.reply(toxic_text.format(toxic=toxic))
