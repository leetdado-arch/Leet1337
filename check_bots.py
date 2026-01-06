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

# Lista botova (username bez @)
BOTS = [
    'leet1337aiwriter_bot',
    'leet1337trade_bot',
    'leet1337code_bot',
    'leet1337general_bot'
]

async def main():
    client = TelegramClient('session_name', API_ID, API_HASH)
    await client.start(phone=PHONE)

    print("Login uspješan. Provjera i dohvat tokena botova, dodavanje u grupe...")

    for username in BOTS:
        print(f"Provjera bota: {username}")

        # Pošalji username u BotFather chat (kao @username da dohvati token)
        await client.send_message('@BotFather', f'@{username}')

        # Čekaj odgovor (povećan na 10 sekundi)
        await asyncio.sleep(10)
        messages = await client.get_messages('@BotFather', limit=10)
        token = None
        for msg in messages:
            if 'You can use this token' in msg.text:
                # Parsiraj token (format: "You can use this token to access HTTP API:\n[token]")
                parts = msg.text.split('HTTP API:\n')
                if len(parts) > 1:
                    token = parts[1].strip().split('\n')[0].split()[0]  # Uzmi prvu riječ tokena
                    print(f"Token dohvaćen za {username}: {token}")
                    break
            elif 'Sorry' in msg.text or 'invalid' in msg.text.lower():
                print(f"Greška za {username}: {msg.text.strip()}")
                break
        else:
            print(f"Nema odgovora za {username}. Bot možda ne postoji ili greška. Preskačem.")
            continue

        if not token:
            print(f"Token za {username} nije dohvaćen. Preskačem.")
            continue

        # Provjeri token pozivom na API (getMe)
        response = requests.get(f'https://api.telegram.org/bot{token}/getMe')
        if response.status_code == 200 and response.json().get('ok'):
            print(f"Token za {username} je validan.")
        else:
            print(f"Token za {username} nije validan: {response.text}")
            continue

        # Dodaj token u .env (ako već ne postoji, overwrite ako treba)
        env_key = f"{username.upper().replace('_', '')}_BOT_TOKEN={token}\n"
        with open('.env', 'a') as f:
            # Provjeri da li već postoji, ako da, zamijeni (jednostavna logika)
            lines = f.readlines() if os.path.exists('.env') else []
            with open('.env', 'w') as f_write:
                for line in lines:
                    if env_key.split('=')[0] not in line:
                        f_write.write(line)
                f_write.write(env_key)
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
