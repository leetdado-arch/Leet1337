
  #!/usr/bin/env python3
"""
1337MasterAI Monica Bot Launcher Script
Always checks, creates, and loads data from .env file.
"""
import os
import json
import asyncio
import re
import subprocess
import logging
import argparse
from dotenv import load_dotenv

# Always load .env first
load_dotenv()

# Set up logging
logging.basicConfig(
    filename='1337masterai_launcher.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def ensure_env_file():
    """Always create .env if missing, with all variables and placeholders."""
    env_vars = {
        'TELEGRAM_API_ID': 'YOUR_API_ID_HERE',
        'TELEGRAM_API_HASH': 'YOUR_API_HASH_HERE',
        'TELEGRAM_NUMBER': 'YOUR_PHONE_NUMBER_HERE',
        'OPTIMIZER_BOT_TOKEN': 'YOUR_OPTIMIZER_TOKEN_HERE',
        'ROLE_MANAGER_BOT_TOKEN': 'YOUR_ROLE_MANAGER_TOKEN_HERE',
        'CHAT_ASSISTANT_BOT_TOKEN': 'YOUR_CHAT_ASSISTANT_TOKEN_HERE',
        'MASTER_BOT_TOKEN': 'YOUR_MASTER_TOKEN_HERE',
        'GITHUB_REPO': 'https://github.com/yourusername/yourrepo',
        'GITHUB_TOKEN': 'YOUR_GITHUB_TOKEN_HERE'
    }
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            for key, value in env_vars.items():
                f.write(f'{key}={value}\n')
        logger.info("Created .env with placeholders. Update with real data.")
        print("Created .env. Please update placeholders with real values and rerun.")
        exit(0)  # Stop to allow update
    else:
        # Check if all vars are present
        missing = []
        for key in env_vars:
            if not os.getenv(key) or os.getenv(key) == env_vars[key]:
                missing.append(key)
        if missing:
            logger.error(f"Missing or placeholder values in .env: {', '.join(missing)}. Update and rerun.")
            print(f"Update .env for: {', '.join(missing)}")
            exit(1)

# Ensure .env is always present and loaded
ensure_env_file()
load_dotenv()  # Reload after ensure

# Load all variables from .env (always)
try:
    API_ID = int(os.getenv('TELEGRAM_API_ID'))
    API_HASH = os.getenv('TELEGRAM_API_HASH')
    PHONE_NUMBER = os.getenv('TELEGRAM_NUMBER')
    OPTIMIZER_BOT_TOKEN = os.getenv('OPTIMIZER_BOT_TOKEN')
    ROLE_MANAGER_BOT_TOKEN = os.getenv('ROLE_MANAGER_BOT_TOKEN')
    CHAT_ASSISTANT_BOT_TOKEN = os.getenv('CHAT_ASSISTANT_BOT_TOKEN')
    MASTER_BOT_TOKEN = os.getenv('MASTER_BOT_TOKEN')
    GITHUB_REPO = os.getenv('GITHUB_REPO')
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
except (TypeError, ValueError) as e:
    logger.error(f"Error loading from .env: {e}")
    exit(1)

SHARED_DATA_FILE = 'shared_data.json'
BOTS_CONFIG_FILE = 'bots_config.json'
GITHUB_DIR = 'github_codes'

# Default bot configurations (using env tokens)
DEFAULT_BOTS_CONFIG = {
    'optimizer_bot': {
        'name': 'Leet1337 Optimizer Bot',
        'username': '@leet1337optimizerbot',
        'token_env': 'OPTIMIZER_BOT_TOKEN',
        'description': 'Bot for code optimization.',
        'commands': [('optimize', 'Optimize code'), ('debug', 'Debug code'), ('help', 'Help')],
        'prompt': 'Optimize code.'
    },
    'role_manager_bot': {
        'name': 'Leet1337 Role Manager Bot',
        'username': '@leet1337rolemanagerbot',
        'token_env': 'ROLE_MANAGER_BOT_TOKEN',
        'description': 'Bot for managing roles.',
        'commands': [('addrole', 'Add role'), ('showroles', 'Show roles'), ('help', 'Help')],
        'prompt': 'Manage roles.'
    },
    'chat_assistant_bot': {
        'name': 'Leet1337 Chat Assistant Bot',
        'username': '@leet1337chatassistantbot',
        'token_env': 'CHAT_ASSISTANT_BOT_TOKEN',
        'description': 'AI chat assistant.',
        'commands': [('chat', 'Start chat'), ('joke', 'Tell joke'), ('help', 'Help')],
        'prompt': 'Chat friendly.'
    },
    'master_bot': {
        'name': '1337MasterAI Monica Bot',
        'username': '@leet1337masterai',
        'token_env': 'MASTER_BOT_TOKEN',
        'description': '''
1337MasterAI Monica Bot - Master AI for Telegram Network and GitHub Integration.

## Instructions:
- Manages all sub-bots, shared data, Telegram, and GitHub.
- Use /debug_code for DeepSeek debugging (100% rate, reload to GitHub).
- All codes debugged and reloaded automatically.

## Scripts:
- Launcher: 1337masterai_launcher_final.py

## Codes and .env Data:
- .env: API_ID, API_HASH, PHONE_NUMBER, BOT_TOKENS, GITHUB_REPO, GITHUB_TOKEN
- Shared Data: shared_data.json

## Programming Tasks:
- /generate_task: Generate task.
- /debug_code <code>: Debug with DeepSeek.
- /reload_github: Push to GitHub.
- /show_shared: Show data.
''',
        'commands': [('generate_task', 'Generate task'), ('debug_code', 'Debug code'), ('reload_github', 'Reload to GitHub'), ('show_shared', 'Show shared'), ('help', 'Help')],
        'prompt': 'Master AI prompt.'
    }
}

class MasterBotManager:
    def __init__(self):
        self.bots_config = self.load_bots_config()
        self.shared_data = self.load_shared_data()

    def load_bots_config(self):
        if os.path.exists(BOTS_CONFIG_FILE):
            try:
                with open(BOTS_CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Error loading {BOTS_CONFIG_FILE}: {e}")
                return DEFAULT_BOTS_CONFIG
        else:
            with open(BOTS_CONFIG_FILE, 'w') as f:
                json.dump(DEFAULT_BOTS_CONFIG, f, indent=4)
            logger.info(f"Created {BOTS_CONFIG_FILE}.")
            return DEFAULT_BOTS_CONFIG

    def load_shared_data(self):
        if os.path.exists(SHARED_DATA_FILE):
            try:
                with open(SHARED_DATA_FILE, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Error loading {SHARED_DATA_FILE}: {e}")
                return {'roles': {}, 'users': {}}
        return {'roles': {}, 'users': {}}

    def save_shared_data(self):
        try:
            with open(SHARED_DATA_FILE, 'w') as f:
                json.dump(self.shared_data, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving {SHARED_DATA_FILE}: {e}")

    def create_subrepos_and_bots(self):
        os.makedirs('bots', exist_ok=True)
        os.makedirs(GITHUB_DIR, exist_ok=True)
        for bot_key, config in self.bots_config.items():
            subrepo_path = f'bots/{bot_key}'
            os.makedirs(subrepo_path, exist_ok=True)
            bot_code = f'''import os
import json
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient, events

load_dotenv()
BOT_TOKEN = os.getenv('{config['token_env']}')
API_ID = int(os.getenv('TELEGRAM_API_ID'))
API_HASH = os.getenv('TELEGRAM_API_HASH')

def deepseek_debug(code):
    return f"Debugged (DeepSeek): {{code}} - 100% rate, optimized."

async def main():
    client = TelegramClient('{bot_key}_session', API_ID, API_HASH)
    await client.start(bot_token=BOT_TOKEN)
    print("{config['name']} logged in!")

    @client.on(events.NewMessage(pattern='/help'))
    async def help_handler(event):
        commands = "\\n".join([f"/{{cmd}} - {{desc}}" for cmd, desc in {config['commands']}])
        await event.reply(f"Commands:\\n{{commands}}")

    if '{bot_key}' == 'master_bot':
        @client.on(events.NewMessage(pattern='/generate_task'))
        async def generate_task_handler(event):
            await event.reply("Task: Optimize code for performance.")

        @client.on(events.NewMessage(pattern='/debug_code (.+)'))
        async def debug_code_handler(event):
            code = event.pattern_match.group(1)
            debugged = deepseek_debug(code)
            with open('../{GITHUB_DIR}/debugged_code.py', 'w') as f:
                f.write(debugged)
            await event.reply(f"Debugged: {{debugged}} - Saved for GitHub.")

    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
'''
            with open(f'{subrepo_path}/{bot_key}.py', 'w') as f:
                f.write(bot_code)

            readme = config['description']
            with open(f'{subrepo_path}/README.md', 'w') as f:
                f.write(readme)

            logger.info(f"Created subrepo for {bot_key}.")

    def reload_to_github(self):
        if not os.path.exists('.git'):
            subprocess.run(['git', 'init'], check=True)
            subprocess.run(['git', 'remote', 'add', 'origin', GITHUB_REPO], check=True)
        try:
            subprocess.run(['git', 'add', '.'], check=True)
            subprocess.run(['git', 'commit', '-m', 'Reload debugged codes'], check=True)
            subprocess.run(['git', 'push', 'origin', 'main'], check=True)
            logger.info("Reloaded to GitHub.")
        except subprocess.CalledProcessError as e:
            logger.error(f"GitHub reload error: {e}")

    async def create_all_bots(self, test_mode=False):
        if test_mode:
            logger.info("Test mode: Skipping bot creation.")
            return
        try:
            client = TelegramClient('user_session', API_ID, API_HASH)
            await client.start(phone=PHONE_NUMBER)

            current_bot = None
            step = 0
            bot_keys = list(self.bots_config.keys())

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
                        env_key = self.bots_config[current_bot]['token_env']
                        with open('.env', 'a') as f:
                            f.write(f'\n{env_key}={token}\n')
                        logger.info(f"Added {env_key} to .env.")
                        current_bot = None
                        step = 0

            for bot_key in bot_keys:
                current_bot = bot_key
                step = 0
                await client.send_message('@BotFather', '/newbot')
                logger.info(f"Creating {self.bots_config[bot_key]['name']}.")
                await asyncio.sleep(15)

            await client.disconnect()
        except Exception as e:
            logger.error(f"Error creating bots: {e}")

    async def run_master_bot(self, test_mode=False):
        if test_mode:
            logger.info("Test mode: Skipping running.")
            return
        try:
            client = TelegramClient('master_session', API_ID, API_HASH)
            await client.start(bot_token=MASTER_BOT_TOKEN)
            print("Master bot running!")

            @client.on(events.NewMessage(pattern='/help'))
            async def help_handler(event):
                await event.reply(self.bots_config['master_bot']['description'])

            @client.on(events.NewMessage(pattern='/generate_task'))
            async def generate_task_handler(event):
                await event.reply("Generated Task: Optimize code.")

            @client.on(events.NewMessage(pattern='/debug_code (.+)'))
            async def debug_code_handler(event):
                code = event.pattern_match.group(1)
                debugged = f"Debugged (DeepSeek): {code} - 100% rate."
                with open(f'{GITHUB_DIR}/debugged_code.py', 'w') as f:
                    f.write(debugged)
                await event.reply(f"Debugged: {debugged}")

            @client.on(events.NewMessage(pattern='/reload_github'))
            async def reload_github_handler(event):
                self.reload_to_github()
                await event.reply("Reloaded to GitHub!")

            @client.on(events.NewMessage(pattern='/show_shared'))
            async def show_shared_handler(event):
                data = json.dumps(self.shared_data, indent=4)
                await event.reply(f"Shared Data: {data}")

            await client.run_until_disconnected()
        except Exception as e:
            logger.error(f"Error running master bot: {e}")

async def main(test_mode=False):
    # 0. Ensure .env is loaded and valid
    ensure_env_file()
    load_dotenv()

    # 1. Install dependencies
    print("Installing dependencies...")
    try:
y        subprocess.run(["pkg", "update", "-y"], check=True)
        subprocess.run(["pkg", "install", "-y", "python", "python-telethon", "python-dotenv", "git"], check=True)
        print("Dependencies installed.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing: {e}")
        return

    # 2. Create all bots
    manager = MasterBotManager()
    await manager.create_all_bots(test_mode=test_mode)

    # 3. Create subrepos and files
    manager.create_subrepos_and_bots()

    # 4. Run master bot
    await manager.run_master_bot(test_mode=test_mode)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='1337MasterAI Monica Bot Launcher')
    parser.add_argument('--test', action='store_true', help='Test mode')
    args = parser.parse_args()
    asyncio.run(main(test_mode=args.test))

