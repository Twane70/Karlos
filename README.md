## Setup
create virtual env (Mac or Windows)

.\venv\Scripts\activate
conda deactivate

pip install -r .\requirements.txt

uvicorn api.main:app --reload




---
TODO : investigate scrambled streaming

```
async def choose_agent_generator(main_query: str):
    async for chunk in choose_agent_chain().astream({'question': main_query}):
        print(chunk, end='|', flush=True)
        yield chunk.encode("utf-8")

@router.get("/streaming")
async def stream():
    return StreamingResponse(choose_agent_generator("pourquoi le ciel est bleu"), media_type="text/plain")
```