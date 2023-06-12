import asyncio
import random
import aiohttp

IdsRequeridos=10

LANGUAGES = {
    'en': ['level'],
    'es': ['nivel'],
    'pt': ['nível'],
    'fr': ['niveau'],
    'de': ['niveau'],
    'it': ['livello'],
    'ru': ['уровень'],
    'ja': ['レベル'],
    'ko': ['레벨'],
    'zh': ['等级']
}

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def check_steam_profiles():
    base_id = 76561197960265728
    found_profiles = []

    async with aiohttp.ClientSession() as session:
        while len(found_profiles) < IdsRequeridos:
            steam_id = str(base_id + random.randint(1, 999999999))
            if len(steam_id) == 17 and steam_id.startswith('7656119'):
                profile_url = f"https://steamcommunity.com/profiles/{steam_id}"
                response = await fetch(session, profile_url)
                if any(any(word in response.lower() for word in LANGUAGES[lang]) for lang in LANGUAGES):
                    found_profiles.append(steam_id)

    return found_profiles


def run_check_steam_profiles():
    loop = asyncio.get_event_loop()
    public_profiles = loop.run_until_complete(check_steam_profiles())
    return public_profiles
