import os
import asyncio
import re
from dotenv import load_dotenv
from telethon import TelegramClient, events
import subprocess

load_dotenv()

# Koristi korisnički account za komunikaciju (botovi ne mogu slati poruke drugim botovima)
API_ID = int(os.getenv('TELEGRAM_API_ID'))
API_HASH = os.getenv('TELEGRAM_API_HASH')
PHONE_NUMBER = os.getenv('TELEGRAM_NUMBER')  # Tvoj broj telefona
BOTFATHER_USERNAME = '@BotFather'

# Parametri za novog bota
NEW_BOT_NAME = 'Leet1337 Optimizer Bot'
NEW_BOT_USERNAME = '@leet1337optimizerbot'
ENV_KEY = 'OPTIMIZER_BOT_TOKEN'

async def create_bot():
    client = TelegramClient('user_session', API_ID, API_HASH)
    await client.start(phone=PHONE_NUMBER)  # Login sa korisničkim account-om
    
    # Počni chat sa @BotFather
    await client.send_message(BOTFATHER_USERNAME, '/newbot')
    print("Poslao /newbot @BotFather-u.")
    
    # Handler za odgovore
    @client.on(events.NewMessage(from_users=BOTFATHER_USERNAME))
    async def handler(event):
        message = event.message.text.lower()  # Case insensitive
        if 'alright, a new bot' in message or 'choose a name' in message:
            await client.send_message(BOTFATHER_USERNAME, NEW_BOT_NAME)
            print(f"Poslao ime bota: {NEW_BOT_NAME}")
        elif 'choose a username' in message:
            await client.send_message(BOTFATHER_USERNAME, NEW_BOT_USERNAME)
            print(f"Poslao username: {NEW_BOT_USERNAME}")
        elif 'use this token' in message:
            # Parsiraj token
            token_match = re.search(r'(\d+:[A-Za-z0-9_-]+)', message)
            if token_match:
                token = token_match.group(1)
                # Dodaj u .env
                with open('.env', 'a') as f:
                    f.write(f'\n{ENV_KEY}={token}\n')
                print(f"Dodao {ENV_KEY}={token} u .env fajl.")
                await client.disconnect()
            else:
                print("Greška: Token nije pronađen.")
    
    # Čekaj 60 sekundi za interakciju (više vremena za login ako treba)
    await asyncio.sleep(60)
    await client.disconnect()

async def upload_to_github():
    repo_name = 'Leet1337-Bots'
    try:
        result = subprocess.run(['gh', 'repo', 'view', repo_name], capture_output=True, text=True)
        if result.returncode != 0:
            subprocess.run(['gh', 'repo', 'create', repo_name, '--public'], check=True)
            print(f"Kreirao GitHub repo: {repo_name}")
        
        subprocess.run(['git', 'add', 'create_bot_via_botfather.py'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Fixed and added create_bot_via_botfather.py'], check=True)
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        print(f"Upload-ovao skriptu na GitHub repo: {repo_name}")
    except subprocess.CalledProcessError as e:
        print(f"Greška u upload-u: {e}")

async def main():
    await create_bot()
    await upload_to_github()

if __name__ == '__main__':
    asyncio.run(main())
