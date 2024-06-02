from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from datetime import datetime, timedelta
import uuid
import logging
import favicon
import tldextract

# custom functions
from utils.objects import SafePromptAsker, Expert, N_QUERIES, Queries, simple_ask
from utils.prompts import auto_agent_instructions, search_queries_prompt, storytelling_instructions
from utils.researcher.scraper import get_results, get_context_by_urls

#logging.basicConfig(level=logging.DEBUG)

load_dotenv()

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:5173",  # local Vite frontend
    "https://supreme-carnival.onrender.com/",  # prod
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Storage for process states
process_states = {}
TASK_EXPIRATION = timedelta(hours=24)

class MainQueryRequest(BaseModel):
    query: str
    lang: str = "french"

def cleanup_old_tasks():
    now = datetime.now()
    for task_id, state in list(process_states.items()):
        if state.get('timestamp') and now - state['timestamp'] > TASK_EXPIRATION:
            del process_states[task_id]

async def generate_expert(main_query, lang):
    expert_generator = SafePromptAsker(
        prompt=auto_agent_instructions(),
        parameters=["topic"],
        pydantic_object=Expert,
        lang=lang,
        model_version='gpt-4o')
    return expert_generator.ask(topic=main_query)

async def generate_queries(expert_description, main_query, lang):
    queries_generator = SafePromptAsker(
        prompt=search_queries_prompt(N_QUERIES),
        parameters=["role", "topic"],
        pydantic_object=Queries,
        lang=lang,
        model_version='gpt-4o')
    return queries_generator.ask(role=expert_description, topic=main_query).queries_list

async def fetch_results_and_sources(queries):
    msg_sources = ""
    sources = []
    for query in queries:
        results = await get_results(query)
        sources += [website['href'] for website in results]
        msg_sources += f'## **{query.capitalize()}**\n'
        msg_sources += '\n'.join([f' - [{website.get("title")}]({website["href"]})' for website in results]) + '\n'
    return msg_sources, sources

async def generate_context(queries, main_query, sources):
    context_chunks = await get_context_by_urls(', '.join(queries + [main_query]), sources)
    context_chunks.sort(key=lambda chunk: chunk.get('source', 'None'))
    context = []
    for id_chunk, chunk in enumerate(context_chunks):
        if chunk.get('content') not in [chunk['content'] for chunk in context]:
            try:
                icons = favicon.get(chunk.get('source'))
                icon = icons[0].url
            except:
                icon = './public/web.png'
            try:
                name_author = tldextract.extract(chunk.get('source')).domain
            except:
                name_author = f'Source {id_chunk + 1}'
            context.append({
                'id': id_chunk + 1,
                'title': chunk.get('title'),
                'author': name_author,
                'content': chunk.get('content'),
                'source': chunk.get('source'),
                'icon': icon
            })
            
            # f"[{id_chunk + 1}] {chunk.get('title')} | {name_author} \n [...] {chunk.get('content')} [...]\n---\n"
    return context

async def generate_summary(main_query, queries, context, lang):
    return simple_ask(
        storytelling_instructions(),
        parameters=['topic', 'subtopics', 'context', 'lang'],
        topic=main_query,
        subtopics=', '.join(queries),
        context='\n---\n'.join([f"[{chunk['id']}] | {chunk['author']}\n[...]{chunk['content']}[...]" for chunk in context]),
        lang=lang,
        model_version='gpt-4o'
    )

@app.post("/start-process")
async def start_process(request: MainQueryRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    process_states[task_id] = {
        "status": "En cours",
        "steps": {},
        "timestamp": datetime.now()
    }
    background_tasks.add_task(run_process, task_id, request.query, request.lang)
    return {"message": "Processus démarré", "task_id": task_id}

@app.get("/process-status/{task_id}")
async def get_process_status(task_id: str):
    if task_id not in process_states:
        raise HTTPException(status_code=404, detail="Task ID not found")
    return process_states[task_id]

async def run_process(task_id, main_query, lang):
    try:
        process_states[task_id]["steps"]["expert"] = "En cours"
        expert = await generate_expert(main_query, lang)
        process_states[task_id]["steps"]["expert"] = expert

        process_states[task_id]["steps"]["queries"] = "En cours"
        queries = await generate_queries(expert.description, main_query, lang)
        process_states[task_id]["steps"]["queries"] = queries

        process_states[task_id]["steps"]["sources"] = "En cours"
        msg_sources, sources = await fetch_results_and_sources(queries)
        process_states[task_id]["steps"]["sources"] = msg_sources
        print(msg_sources)

        process_states[task_id]["steps"]["context"] = "En cours"
        context = await generate_context(queries, main_query, sources)
        process_states[task_id]["steps"]["context"] = context

        process_states[task_id]["steps"]["summary"] = "En cours"
        summary = await generate_summary(main_query, queries, context, lang)
        process_states[task_id]["steps"]["summary"] = summary

        process_states[task_id]["status"] = "Terminé"
    except Exception as e:
        logging.error(f"ERROR with task {task_id} : {e}")
        process_states[task_id]["status"] = "Échoué"
        process_states[task_id]["error"] = str(e)
    finally:
        cleanup_old_tasks()
