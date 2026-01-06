  #!/usr/bin/env python3
  """
  Script za Provjeru Nedostajućih Bot Tokena
  Koristi se za skeniranje .env fajla i pronalaženje praznih ili placeholder tokena za bote.
  """
  import os
  from dotenv import load_dotenv

  # Učitaj .env fajl
  load_dotenv()

  # Lista svih bot tokena koje provjeravamo
  bot_tokens = [
      'OPTIMIZER_BOT_TOKEN',
      'ROLE_MANAGER_BOT_TOKEN',
      'CHAT_ASSISTANT_BOT_TOKEN',
      'MASTER_BOT_TOKEN'
  ]

  # Placeholder vrijednosti (ako su još uvijek ove, token je missing)
  placeholders = {
      'OPTIMIZER_BOT_TOKEN': 'YOUR_OPTIMIZER_TOKEN_HERE',
      'ROLE_MANAGER_BOT_TOKEN': 'YOUR_ROLE_MANAGER_TOKEN_HERE',
      'CHAT_ASSISTANT_BOT_TOKEN': 'YOUR_CHAT_ASSISTANT_TOKEN_HERE',
      'MASTER_BOT_TOKEN': 'YOUR_MASTER_TOKEN_HERE'
  }

  def check_missing_tokens():
      """Provjeri i ispisi missing tokene."""
      missing = []
      print("Provjeravam bot tokene u .env fajlu...")
      for token_key in bot_tokens:
          token_value = os.getenv(token_key)
          if not token_value or token_value == placeholders[token_key]:
              missing.append(token_key)
              print(f"✗ {token_key}: Missing ili placeholder vrijednost.")
          else:
              print(f"✓ {token_key}: OK ({token_value[:10]}...)")  # Prikaži samo početak za sigurnost
      if missing:
          print(f"\nNedostajući tokene: {', '.join(missing)}")
          print("Update .env fajl sa pravim vrijednostima i pokreni ponovo.")
      else:
          print("\nSvi bot tokene su prisutni!")
      return missing

  if __name__ == '__main__':
      check_missing_tokens()
