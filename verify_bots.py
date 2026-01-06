import os
import asyncio
import requests
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

# Učitaj iz .env
API_ID = int(os.getenv('TELEGRAM_API_ID', '38139627'))
API_HASH = os.getenv('TELEGRAM_API_HASH', '2a94a8e2df827a90146ec1a000571978')
PHONE = os.getenv('TELEGRAM_NUMBER')
GROUP_IDS_STR = os.getenv('TELEGRAM_GROUP_IDS', '')  # Lista ID-ova, npr. "-1003318405048,-1003547237727,-1003549899659"
GROUP_IDS = [int(id.strip()) for id in GROUP_IDS_STR.split(',') if id.strip()] if GROUP_IDS_STR else []

# Lista botova sa tokenima (iz tvog chata sa BotFather-om)
BOTS_TOKENS = {
    'leet1337aiwriter_bot': '8546769466:AAGlfqBJ7j3-QGYIdNjVCG3u7krjfaOmPEU',
    'leet1337trade_bot': '8546769466:AAGlfqBJ7j3-QGYIdNjVCG3u7krjfaOmPEU',  # Isti kao aiwriter? Ako greška, podijeli ispravne
    'leet1337code_bot': '8516734292:AAEG2rsbLzOI-zJ2fYBxQvqu-8a2ORFcWUw',
    'leet1337general_bot': '8581832928:AAHXQ7opQvSEIgf_zGcO3Fvxwgk-5eWN3b0'
}

async def main():
    client = TelegramClient('session_name', API_ID, API_HASH)
    await client.start(phone=PHONE)

    print("Login uspješan. Provjera tokena, upload u .env, dodavanje u grupe...")

    for username, token in BOTS_TOKENS.items():
        print(f"Provjera bota: {username} sa tokenom: {token}")

        # Provjeri token pozivom na API (getMe)
        response = requests.get(f'https://api.telegram.org/bot{token}/getMe')
        if response.status_code == 200 and response.json().get('ok'):
            print(f"Token za {username} je validan.")
        else:
            print(f"Token za {username} nije validan: {response.text}")
            continue

        # Dodaj token u .env (overwrite ako postoji)
        env_key = f"{username.upper().replace('_', '')}_BOT_TOKEN={token}\n"
        lines = []
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                lines = f.readlines()
        with open('.env', 'w') as f:
            for line in lines:
                if not line.startswith(env_key.split('=')[0] + '='):
                    f.write(line)
            f.write(env_key)
        print(f"Token za {username} dodan/u .env fajl.")

        # Dodaj bota u sve grupe iz liste (ako nije već)
        for group_id in GROUP_IDS:
            try:
                await client.invite_to_channel(group_id, username)
                print(f"Bot {username} dodan u grupu {group_id}.")
            except Exception as e:
                print(f"Greška pri dodavanju u grupu {group_id}: {e} (možda već dodan)")

    await client.disconnect()
    print("Provjera završena. Tokene provjeri u .env fajlu.")

if __name__ == '__main__':
    asyncio.run(main())
