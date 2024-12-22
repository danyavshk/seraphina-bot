import os
import logging
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv('AI_TOKEN'))
logger = logging.getLogger(__name__)

async def gpt4(question):
    try:
        response = await client.chat.completions.create(
            messages=[{"role": "user", "content": str(question)}],
            model=os.getenv('OPENAI_MODEL', 'gpt-4')  # Поддержка кастомной модели через .env
        )
        return response
    except Exception as e:
        logger.error(f"Ошибка при вызове OpenAI API: {e}")
        return None
