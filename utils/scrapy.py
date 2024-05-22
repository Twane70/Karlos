import asyncio
import aiohttp

from bs4 import BeautifulSoup
from duckduckgo_search import AsyncDDGS


async def get_results(query):
    async with AsyncDDGS() as ddgs:
        results = [r async for r in ddgs.text(query, max_results=3)]
        return results



def invalidate(url):
    sites_relous = ['.pdf', 'theses.hal.science',
                    'www.pinterest', 'www.instagram', 'quora.com', 'reddit.com','www.netflix','www.spotify','www.hulu','www.hbomax','www.tripadvisor','www.yelp','www.disneyplus']
    if any(site in url for site in sites_relous):
            print(f"URL ignorée : {url}")
            return True
    else:
        return False


def parse_content(html, max_len=10000):
    soup = BeautifulSoup(html, 'lxml')
    content = ""

    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']):
        if len(content) >= max_len:
            print("...")
            break

        if tag.name.startswith('h'):
            content += f"{'#' * (int(tag.name[1:]) + 1)} {tag.get_text()}\n"
        else:
            content += f"{tag.get_text()}\n"

    lines = (line.strip() for line in content.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    content = "\n".join(chunk for chunk in chunks if chunk)
    return content


async def fetch(session, url):
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        print(f"Request failed for {url}: {e}")
        return ''

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)
