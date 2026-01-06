import os
  import json
  import asyncio
  import re
  import subprocess
  from dotenv import load_dotenv
  from telethon import TelegramClient, events

  load_dotenv()

  # Učitaj sve iz .env fajla
  API_ID = int(os.getenv('TELEGRAM_API_ID'))
  API_HASH = os.getenv('TELEGRAM_API_HASH')
  PHONE_NUMBER = os.getenv('TELEGRAM_NUMBER')
  BOT_TOKENS = {}  # Dinamički puni token-e za svakog bota

  # Zajednički fajl za dijeljene podatke (role-e, korisnici, itd.)
  SHARED_DATA_FILE = 'shared_data.json'

  # Definisanje botova sa opisima, opcijama i prompt-ima
  BOTS_CONFIG = {
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

  # Učitaj dijeljene podatke
  def load_shared_data():
      if os.path.exists(SHARED_DATA_FILE):
          with open(SHARED_DATA_FILE, 'r') as f:
              return json.load(f)
      return {'roles': {}, 'users': {}}

  # Spremi dijeljene podatke
  def save_shared_data(data):
      with open(SHARED_DATA_FILE, 'w') as f:
          json.dump(data, f, indent=4)

  # Kreiraj subrepo za svakog bota
  def create_subrepo(bot_key, bot_config):
      subrepo_path = f'bots/{bot_key}'
      os.makedirs(subrepo_path, exist_ok=True)
      
      # Kreiraj bot kod fajl u subrepo-u
      bot_code = f'''
  import os
  import json
  import asyncio
  from dotenv import load_dotenv
  from telethon import TelegramClient, events

  load_dotenv()
  BOT_TOKEN = os.getenv('{bot_key.upper()}_BOT_TOKEN')
  API_ID = int(os.getenv('TELEGRAM_API_ID'))
  API_HASH = os.getenv('TELEGRAM_API_HASH')

  SHARED_DATA_FILE = '../shared_data.json'  # Dijeljeni fajl

  def load_shared_data():
      if os.path.exists(SHARED_DATA_FILE):
          with open(SHARED_DATA_FILE, 'r') as f:
              return json.load(f)
      return {{'roles': {{}}, 'users': {{}}}}

  def save_shared_data(data):
      with open(SHARED_DATA_FILE, 'w') as f:
          json.dump(data, f, indent=4)

  async def main():
      client = TelegramClient('{bot_key}_session', API_ID, API_HASH)
      await client.start(bot_token=BOT_TOKEN)
      print("{bot_config['name']} je ulogovan!")

      @client.on(events.NewMessage(pattern='/help'))
      async def help_handler(event):
          commands = "\\n".join([f"/{{cmd}} - {{desc}}" for cmd, desc in {bot_config['commands']}])
          await event.reply(f"Komande za {bot_config['name']}:\\n{{commands}}")

      # Dodaj specifične handlere za svakog bota
      if '{bot_key}' == 'optimizer_bot':
          @client.on(events.NewMessage(pattern='/optimize (.+)'))
          async def optimize_handler(event):
              code = event.pattern_match.group(1)
              # AI prompt za optimizaciju
              response = "{bot_config['prompt']} Optimizuj ovaj kod: {{code}}"
              # Simuliraj AI odgovor (integriraj grok ako treba)
              await event.reply("Optimizovani kod: [primjer]")

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
              # AI prompt za chat
              response = "{bot_config['prompt']} Odgovori na: {{query}}"
              await event.reply("AI odgovor: Ovo je simulacija - integriraj grok za prave odgovore.")

      await client.run_until_disconnected()

  if __name__ == '__main__':
      asyncio.run(main())
  '''
      with open(f'{subrepo_path}/{bot_key}.py', 'w') as f:
          f.write(bot_code)
      
      # Kreiraj README u subrepo-u
      readme = f'''
  # {bot_config['name']}
  {bot_config['description']}

  ## Prompt
  {bot_config['prompt']}

  ## Opcije
  Komande: {', '.join([cmd for cmd, _ in bot_config['commands']])}
  '''
      with open(f'{subrepo_path}/README.md', 'w') as f:
          f.write(readme)
      
      print(f"Kreiran subrepo za {bot_key}: {subrepo_path}")

  # Kreiraj botove preko @BotFather-a
  async def create_bots():
      client = TelegramClient('user_session', API_ID, API_HASH)
      await client.start(phone=PHONE_NUMBER)
      
      for bot_key, config in BOTS_CONFIG.items():
          await client.send_message('@BotFather', '/newbot')
          print(f"Poslao /newbot za {config['name']}.")
          
          @client.on(events.NewMessage(from_users='@BotFather'))
          async def handler(event):
              message = event.message.text.lower()
              if 'choose a name' in message:
                  await client.send_message('@BotFather', config['name'])
              elif 'choose a username' in message:
                  await client.send_message('@BotFather', config['username'])
              elif 'use this token' in message:
                  token_match = re.search(r'(\\d+:[A-Za-z0-9_-]+)', message)
                  if token_match:
                      token = token_match.group(1)
                      BOT_TOKENS[bot_key] = token
                      # Dodaj u .env
                      with open('.env', 'a') as f:
                          f.write(f'\\n{bot_key.upper()}_BOT_TOKEN={token}\\n')
                      print(f"Dodao token za {bot_key}.")
                      await client.disconnect()
          
          await asyncio.sleep(10)  # Čekaj za svakog bota
      
      await client.disconnect()

  # Pokreni sve botove
  async def run_all_bots():
      tasks = []
      for bot_key in BOTS_CONFIG:
          subrepo_path = f'bots/{bot_key}'
          if os.path.exists(f'{subrepo_path}/{bot_key}.py'):
              # Pokreni svakog bota u pozadini
              process = subprocess.Popen(['python', f'{subrepo_path}/{bot_key}.py'])
              tasks.append(process)
      await asyncio.gather(*[asyncio.create_subprocess_exec('sleep', 'infinity') for _ in tasks])  # Drži ih pokrenutim

  async def main():
      # Kreiraj subrepo-e i kodove
      for bot_key, config in BOTS_CONFIG.items():
          create_subrepo(bot_key, config)
      
      # Kreiraj botove
      await create_bots()
      
      # Pokreni botove
      await run_all_bots()

  if __name__ == '__main__':
      asyncio.run(main())
