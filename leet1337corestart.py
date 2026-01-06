#!/usr/bin/env python3
"""
Leet1337 Core Start Script
Kreira, konfigurira i pokreće više Telegram botova sa dijeljenim podacima.
Koristi grok za AI funkcionalnosti.
"""
import os
import json
import asyncio
import re
import subprocess
import logging
import argparse
from dotenv import load_dotenv
from telethon import TelegramClient, events

Postavi logging
logging.basicConfig(
filename='leet1337corestart.log',
level=logging.INFO,
format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(name)

load_dotenv()

Provjera .env fajla
if not os.path.exists('.env'):
logger.error(".env fajl ne postoji. Kreiraj ga sa API_ID, API_HASH, PHONE_NUMBER.")
exit(1)

Učitaj sve iz .env fajla
try:
API_ID = int(os.getenv('TELEGRAM_API_ID'))
API_HASH = os.getenv('TELEGRAM_API_HASH')
PHONE_NUMBER = os.getenv('TELEGRAM_NUMBER')
except (TypeError, ValueError) as e:
logger.error(f"Greška u učitavanju iz .env: {e}")
exit(1)

BOT_TOKENS = {}
SHARED_DATA_FILE = 'shared_data.json'
BOTS_CONFIG_FILE = 'bots_config.json'

Default konfiguracija botova (ako bots_config.json ne postoji)
DEFAULT_BOTS_CONFIG = {
'optimizer_bot': {
'name': 'Leet1337 Optimizer Bot',
'username': '@leet1337optimizerbot',
'description': 'Bot za optimizaciju koda i rješavanje problema u programiranju. Koristi AI za najbolje savjete.',
'commands': [
('optimize', 'Optimizuj kod'),
('debug', 'Debug kod'),
('help', 'Pomoć')
],
'prompt': 'Ti si AI asistent za optimizaciju koda. Daj kratke, efikasne odgovore sa primjerima. Koristi Python i najbolje prakse.'
},
'role_manager_bot': {
'name': 'Leet1337 Role Manager Bot',
'username': '@leet1337rolemanagerbot',
'description': 'Bot za upravljanje role-ama korisnika u grupama. Dodaj ili ukloni role-e sa jednostavnim komandama.',
'commands': [
('addrole', 'Dodaj role korisniku'),
('removerole', 'Ukloni role'),
('showroles', 'Prikaži role-e'),
('help', 'Pomoć')
],
'prompt': 'Ti upravljaš role-ama. Budi striktan i sigurnosno orijentisan. Provjeri dozvole prije akcije.'
},
'chat_assistant_bot': {
'name': 'Leet1337 Chat Assistant Bot',
'username': '@leet1337chatassistantbot',
'description': 'AI chat asistent za opće razgovore, savjete i zabavu. Koristi najnovije informacije.',
'commands': [
('chat', 'Započni razgovor'),
('joke', 'Ispričaj vic'),
('help', 'Pomoć')
],
'prompt': 'Ti si prijateljski AI asistent. Odgovaraj zabavno, informativno i korisno. Koristi emoji-e za bolju komunikaciju.'
}
}

class BotManager:
def init(self):
self.bots_config = self.load_bots_config()
self.shared_data = self.load_shared_data()

def load_bots_config(self):
    if os.path.exists(BOTS_CONFIG_FILE):
        try:
            with open(BOTS_CONFIG_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Greška u učitavanju {BOTS_CONFIG_FILE}: {e}")
            return DEFAULT_BOTS_CONFIG
    else:
        with open(BOTS_CONFIG_FILE, 'w') as f:
            json.dump(DEFAULT_BOTS_CONFIG, f, indent=4)
        logger.info(f"Kreiran {BOTS_CONFIG_FILE} sa default konfiguracijom.")
        return DEFAULT_BOTS_CONFIG

def load_shared_data(self):
    if os.path.exists(SHARED_DATA_FILE):
        try:
            with open(SHARED_DATA_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Greška u učitavanju {SHARED_DATA_FILE}: {e}")
            return {'roles': {}, 'users': {}}
    return {'roles': {}, 'users': {}}

def save_shared_data(self):
    try:
        with open(SHARED_DATA_FILE, 'w') as f:
            json.dump(self.shared_data, f, indent=4)
    except Exception as e:
        logger.error(f"Greška u spremanju {SHARED_DATA_FILE}: {e}")

def create_subrepo(self, bot_key, bot_config):
    try:
        subrepo_path = f'bots/{bot_key}'
        os.makedirs(subrepo_path, exist_ok=True)

        # Kreiraj bot kod fajl (sa grok integracijom)
        bot_code = f'''import os
import json
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient, events

load_dotenv()
BOT_TOKEN = os.getenv('{bot_key.upper()}_BOT_TOKEN')
API_ID = int(os.getenv('TELEGRAM_API_ID'))
API_HASH = os.getenv('TELEGRAM_API_HASH')
SHARED_DATA_FILE = '../shared_data.json'

def load_shared_data():
if os.path.exists(SHARED_DATA_FILE):
with open(SHARED_DATA_FILE, 'r') as f:
return json.load(f)
return {{'roles': {{}}, 'users': {{}}}}

def save_shared_data(data):
with open(SHARED_DATA_FILE, 'w') as f:
json.dump(data, f, indent=4)

Grok-like AI funkcija (simulirana)
def grok_response(prompt, query):
# Koristi prompt za generisanje odgovora (kratko, efikasno)
if 'optimizuj' in prompt.lower():
return f"Optimizovani kod: {{query}} (koristi list comprehension za bolje performanse)."
elif 'chat' in prompt.lower():
return f"AI odgovor: {{query}} - Ja sam grok, uvijek pomažem! 😊"
else:
return "Odgovor: Simulacija grok-a."

async def main():
client = TelegramClient('{bot_key}_session', API_ID, API_HASH)
await client.start(bot_token=BOT_TOKEN)
print("{bot_config['name']} je ulogovan!")

@client.on(events.NewMessage(pattern='/help'))
async def help_handler(event):
    commands = "\\n".join([f"/{{cmd}} - {{desc}}" for cmd, desc in {bot_config['commands']}])
    await event.reply(f"Komande za {bot_config['name']}:\\n{{commands}}")

# Specifični handler-i sa grok integracijom
if '{bot_key}' == 'optimizer_bot':
    @client.on(events.NewMessage(pattern='/optimize (.+)'))
    async def optimize_handler(event):
        code = event.pattern_match.group(1)
        response = grok_response("{bot_config['prompt']}", code)
        await event.reply(response)

elif '{bot_key}' == 'role_manager_bot':
    @client.on(events.NewMessage(pattern='/addrole (\\d+) (.+)'))
    async def add_role_handler(event):
        user_id = int(event.pattern_match.group(1))
        role = event.pattern_match.group(2)
        data = load_shared_data()
        data['roles'][str(user_id)] = role
        save_shared_data(data)
        await event.reply(f"Dodana role '{{role}}' za {{user_id}}.")

    @client.on(events.NewMessage(pattern='/showroles'))
    async def show_roles_handler(event):
        data = load_shared_data()
        roles = data.get('roles', {{}})
        if roles:
            role_list = "\\n".join([f"User {{uid}}: {{role}}" for uid, role in roles.items()])
            await event.reply(f"Role-e:\\n{{role_list}}")
        else:
            await event.reply("Nema role-a.")

elif '{bot_key}' == 'chat_assistant_bot':
    @client.on(events.NewMessage(pattern='/chat (.+)'))
    async def chat_handler(event):
        query = event.pattern_match.group(1)
        response = grok_response("{bot_config['prompt']}", query)
        await event.reply(response)

await client.run_until_disconnected()
if name == 'main':
asyncio.run(main())
'''
with open(f'{subrepo_path}/{bot_key}.py', 'w') as f:
f.write(bot_code)

        # Kreiraj README
        readme = f'''
{bot_config['name']}
{bot_config['description']}

Prompt
{bot_config['prompt']}

Opcije
Komande: {', '.join([cmd for cmd, _ in bot_config['commands']])}
'''
with open(f'{subrepo_path}/README.md', 'w') as f:
f.write(readme)

        logger.info(f"Kreiran subrepo za {bot_key}: {subrepo_path}")
    except Exception as e:
        logger.error(f"Greška u kreiranju subrepo-a za {bot_key}: {e}")

async def create_bots(self, test_mode=False):
    if test_mode:
        logger.info("Test mode: Preskačem kreiranje botova.")
        return
    try:
        client = TelegramClient('user_session', API_ID, API_HASH)
        await client.start(phone=PHONE_NUMBER)

        current_bot = None
        step = 0

        @client.on(events.NewMessage(from_users='@BotFather'))
        async def handler(event):
            nonlocal current_bot, step
            message = event.message.text.lower()
            if current_bot and step == 0 and 'choose a name' in message:
                await client.send_message('@BotFather', self.bots_config[current_bot]['name'])
                step = 1
            elif current_bot and step == 1 and 'choose a username' in message:
                await client.send_message('@BotFather', self.bots_config[current_bot]['username'])
                step = 2
            elif current_bot and step == 2 and 'use this token' in message:
                token_match = re.search(r'(\\d+:[A-Za-z0-9_-]+)', message)
                if token_match:
                    token = token_match.group(1)
                    BOT_TOKENS[current_bot] = token
                    with open('.env', 'a') as f:
                        f.write(f'\\n{current_bot.upper()}_BOT_TOKEN={token}\\n')
                    logger.info(f"Dodao token za {current_bot}.")
                    current_bot = None
                    step = 0

        for bot_key in self.bots_config:
            current_bot = bot_key
            step = 0
            await client.send_message('@BotFather', '/newbot')
            logger.info(f"Poslao /newbot za {self.bots_config[bot_key]['name']}.")
            await asyncio.sleep(15)

        await client.disconnect()
    except Exception as e:
        logger.error(f"Greška u kreiranju botova: {e}")

async def run_all_bots(self, test_mode=False):
    if test_mode:
        logger.info("Test mode: Preskačem pokretanje botova.")
        return
    try:
        processes = []
        for bot_key in self.bots_config:
            subrepo_path = f'bots/{bot_key}'
            if os.path.exists(f'{subrepo_path}/{bot_key}.py'):
                process = subprocess.Popen(['python', f'{subrepo_path}/{bot_key}.py'])
                processes.append(process)
        # Čekaj sa timeout-om
        await asyncio.wait_for(asyncio.gather(*[asyncio.create_subprocess_exec('wait') for _ in processes]), timeout=3600)
    except Exception as e:
        logger.error(f"Greška u pokretanju botova: {e}")
async def main(test_mode=False):
manager = BotManager()

# Prvo kreiraj direktorije
os.makedirs('bots', exist_ok=True)
for bot_key, config in manager.bots_config.items():
    manager.create_subrepo(bot_key, config)

# Kreiraj botove
await manager.create_bots(test_mode=test_mode)

# Pokreni botove
await manager.run_all_bots(test_mode=test_mode)
if name == 'main':
parser = argparse.ArgumentParser(description='Leet1337 Core Start Script')
parser.add_argument('--test', action='store_true', help='Pokreni u test modu (bez botova i pokretanja)')
args = parser.parse_args()
asyncio.run(main(test_mode=args.test))
