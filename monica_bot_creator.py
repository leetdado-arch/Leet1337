import os
import asyncio
import argparse
from dotenv import load_dotenv
from telethon import TelegramClient

# Učitaj .env fajl
load_dotenv()

class MonicaBotCreator:
    def __init__(self):
        self.api_id = int(os.getenv('TELEGRAM_API_ID'))
        self.api_hash = os.getenv('TELEGRAM_API_HASH')
        self.phone = os.getenv('TELEGRAM_NUMBER')
        self.client = TelegramClient('monica_session', self.api_id, self.api_hash)

    async def login_telegram(self):
        """Login u Telegram sa Telethon."""
        await self.client.start(self.phone)
        print("Ulogovan u Telegram!")

    def generate_bot_code(self, name, description, prompt):
        """Koristi AI da generiše bot kod."""
        import openai
        openai.api_key = os.getenv('OPENAI_API_KEY')
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY nije postavljen u .env fajlu.")
        
        full_prompt = f"""
        Kreiraj Python kod za Telegram bota koristeći Telethon biblioteku.
        Bot ime: {name}
        Opis: {description}
        Prompt: {prompt}
        Kod mora uključivati:
        - Import telethon, asyncio, os, dotenv
        - Učitavanje tokena iz .env (npr. BOT_TOKEN)
        - Handler za /start komandu
        - Async main funkcija sa client.start() i client.run_until_disconnected()
        - Koristi markdown za komentare.
        Vrati samo kod, bez dodatnog teksta.
        """
        
        try:
            response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",  # Promijenjeno sa text-davinci-003 ako ne radi
                prompt=full_prompt,
                max_tokens=1000,
                temperature=0.7
            )
            code = response.choices[0].text.strip()
            return code
        except Exception as e:
            print(f"Greška u AI generisanju: {e}")
            return None

    def save_bot_code(self, name, code):
        """Sačuvaj generisani kod u fajl."""
        filename = f"{name.lower().replace(' ', '_')}_bot.py"
        with open(filename, 'w') as f:
            f.write(code)
        print(f"Kod za {name} sačuvan u {filename}.")
        return filename

    async def deploy_bot(self, token, filename):
        """Deploy bot (test pokretanja)."""
        print(f"Deploy {filename} sa tokenom {token[:10]}...")  # Sakrij puni token za sigurnost
        # Primjer: Pokreni skriptu (opciono, komentarisano da ne bude opasno)
        # os.system(f"python {filename}")

    async def create_bot(self, name, description, prompt):
        """Cijeli proces kreiranja i deploy-a."""
        print(f"Kreiram bota: {name}")
        # Generiši kod
        code = self.generate_bot_code(name, description, prompt)
        if not code:
            print("Neuspjelo generisanje koda.")
            return
        # Sačuvaj kod
        filename = self.save_bot_code(name, code)
        # Dodaj token u .env (pretpostavimo da je već tu)
        token_key = f"{name.upper().replace(' ', '').replace('_', '')}_BOT_TOKEN"
        token = os.getenv(token_key)
        if not token:
            print(f"Greška: Token za {name} nije u .env fajlu (ključ: {token_key}).")
            return
        # Deploy
        await self.deploy_bot(token, filename)
        print(f"Bot {name} kreiran i deploy-an!")

async def main():
    parser = argparse.ArgumentParser(description="Monica Bot Creator")
    parser.add_argument('--create-bot', action='store_true', help="Kreiraj novi bot")
    parser.add_argument('--name', type=str, help="Ime bota")
    parser.add_argument('--description', type=str, help="Opis bota")
    parser.add_argument('--prompt', type=str, help="Prompt za AI generisanje")

    args = parser.parse_args()

    creator = MonicaBotCreator()
    await creator.login_telegram()

    if args.create_bot:
        if not all([args.name, args.description, args.prompt]):
            print("Greška: Navedi --name, --description, --prompt")
            return
        await creator.create_bot(args.name, args.description, args.prompt)

    await creator.client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())

