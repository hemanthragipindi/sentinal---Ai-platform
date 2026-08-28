import asyncio
from app.ai.llm.huggingface import HuggingFaceLLM
from app.core.config import settings

async def test():
    try:
        print(f"Using Token: {settings.HF_TOKEN}")
        print(f"Using Model: {settings.LLM_MODEL_NAME}")
        llm = HuggingFaceLLM()
        print("Sending prompt to HF...")
        res = await llm.generate_response('Hello')
        print("Response:", res)
    except Exception as e:
        print("Exception caught:", e)

if __name__ == "__main__":
    asyncio.run(test())
