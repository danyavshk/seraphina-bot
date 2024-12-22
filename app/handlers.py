from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from app.generators import gpt4
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()

class Generate(StatesGroup):
    text = State()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
        f'Привет, {message.from_user.first_name}! \n'
        f'Я Серафина, твой помощник по изучению курса ИИ. \n'
        f'В боте встроен API OpenAI. Напишите ваш запрос!\n\n'
        f'🎓 Полезные материалы:\n'
        f'- [Интерактивное видео по ИИ](https://an1.h5p.com/content/1292451115818241327/embed)\n'
        f'- [Тест по курсу ИИ](https://an1.h5p.com/content/1292455030239160407/embed)',
        parse_mode="Markdown"
    )
    await state.clear()

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "🛠 Команды и возможности бота:\n\n"
        "/start - Запустить бота и начать диалог.\n"
        "/help - Показать это сообщение помощи.\n\n"
        "📚 Как пользоваться:\n"
        "1. Напишите любой вопрос, и я постараюсь дать вам развернутый ответ.\n"
        "2. Если вы хотите узнать больше о какой-то теме в области ИИ, просто опишите свой запрос.\n\n"
        "💡 Примеры запросов:\n"
        "- \"Объясни, как работает нейронная сеть.\"\n"
        "- \"Приведи пример кода для обучения модели классификации в Python.\"\n"
        "- \"Что такое алгоритм градиентного спуска?\"\n\n"
        "Если у вас возникли проблемы или вопросы, просто напишите мне, и я постараюсь помочь! 😊"
    )

@router.message(Generate.text)
async def generate_error(message: Message):
    await message.answer('Подождите, происходит генерация ответа по вашему запросу...')

@router.message(F.text)
async def generate(message: Message, state: FSMContext):
    await state.set_state(Generate.text)
    response = await gpt4(message.text)
    await message.answer(response.choices[0].message.content)
    await state.clear()
