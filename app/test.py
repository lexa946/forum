import aiohttp
import asyncio






async def main():
    async with aiohttp.ClientSession() as session:
        async with session.post(f"http://127.0.0.1:8000/forum/api/v1/comment", data={
            "thread_id": 100,"text": "dawdawdawdwadawd","nick": "Анон",
        }) as response:
            text = await response.text()
            print(text)



asyncio.run(main())



