import os
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

# Učitaj iz .env
API_ID = int(os.getenv('TELEGRAM_API_ID', '38139627'))
API_HASH = os.getenv('TELEGRAM_API_HASH', '2a94a8e2df827a90146ec1a000571978')
PHONE = os.getenv('TELEGRAM_NUMBER')
GROUP_IDS_STR = os.getenv('TELEGRAM_GROUP_IDS', '')  # Lista ID-ova, npr. "-1003318405048,-1003547237727,-1003549899659"
GROUP_IDS = [int(id.strip()) for id in GROUP_IDS_STR.split(',') if id.strip()] if GROUP_IDS_STR else []

# Lista botova (display_name, username, description)
BOTS = [
    ('Leet1337 AI Writer Bot', 'leet1337aiwriter_bot', 'AI bot za pisanje teksta i članaka'),
    ('Leet1337 Trade Bot', 'leet1337trade_bot', 'AI bot za trading i finansijske operacije'),
    ('Leet1337 Code Bot', 'leet1337code_bot', 'AI bot za generisanje koda i debugging'),
    ('Leet1337 General Bot', 'leet1337general_bot', 'Generalni AI bot za chat i taskove')
]

async def main():
    client = TelegramClient('session_name', API_ID, API_HASH)
    await client.start(phone=PHONE)

    print("Login uspješan. Kreiranje botova i dodavanje u sve grupe...")

    for display_name, username, desc in BOTS:
        print(f"Kreiranje bota: {username}")

        # Pošalji /newbot
        await client.send_message('@BotFather', '/newbot')

        # Čekaj i pošalji display name
        await asyncio.sleep(3)
        await client.send_message('@BotFather', display_name)

        # Čekaj i pošalji username (sa _bot)
        await asyncio.sleep(3)
        await client.send_message('@BotFather', username)

        # Čekaj i pošalji opis
        await asyncio.sleep(3)
        await client.send_message('@BotFather', desc)

        # Čekaj odgovor i dohvati token (povećan limit na 10 za sigurnost)
        await asyncio.sleep(10)
        messages = await client.get_messages('@BotFather', limit=10)
        token = None
        for msg in messages:
            if 'Use this token' in msg.text:
                parts = msg.text.split('Use this token to access the HTTP API: ')
                if len(parts) > 1:
                    token = parts[1].strip().split()[0]  # Uzmi samo token (prvu riječ ako ima više)
                    print(f"Token za {username}: {token}")

                    # Dodaj u .env (uppercase username bez _ + _BOT_TOKEN)
                    env_key = f"{username.upper().replace('_', '')}_BOT_TOKEN={token}\n"
                    with open('.env', 'a') as f:
                        f.write(env_key)
                    print(f"Dodan u .env: {env_key.strip()}")
                    break
        else:
            print(f"Greška: Token za {username} nije dohvaćen (moguće da username postoji ili greška). Preskačem dodavanje. Promijeni username u skripti.")
            continue

        # Dodaj bota u sve grupe iz liste
        for group_id in GROUP_IDS:
            try:
                await client.invite_to_channel(group_id, username)
                print(f"Bot {username} dodan u grupu {group_id}.")
            except Exception as e:
                print(f"Greška pri dodavanju u grupu {group_id}: {e}")

    await client.disconnect()
    print("Svi botovi kreirani i dodani u sve grupe. Provjeri .env fajl i grupe.")

if __name__ == '__main__':
    asyncio.run(main())
