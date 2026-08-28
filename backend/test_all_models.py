import asyncio
from huggingface_hub import AsyncInferenceClient
from app.core.config import settings

async def main():
    token = settings.HF_TOKEN
    client = AsyncInferenceClient(token=token)
    
    models = [
        "Qwen/Qwen2.5-72B-Instruct",
        "Qwen/Qwen2.5-7B-Instruct",
        "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
        "mistralai/Mistral-7B-Instruct-v0.3",
        "mistralai/Mistral-Nemo-Instruct-2407",
        "meta-llama/Llama-3.1-8B-Instruct",
        "google/gemma-2-9b-it"
    ]
    
    for model in models:
        print(f"\nTesting {model}...")
        try:
            res = await client.chat_completion(
                model=model,
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=10
            )
            print(f"✅ SUCCESS: {model}")
            print(f"Response: {res.choices[0].message.content}")
        except Exception as e:
            print(f"❌ FAILED: {model}")
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
