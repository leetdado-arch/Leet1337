#!/bin/bash

# Učitaj varijable iz .env
source .env

# Telegram broj iz .env
TELEGRAM_PHONE=$TELEGRAM_NUMBER

# Lista botova za kreiranje (ime bota i opis)
BOTS=(
  "LeetAIWriterBot AI bot za pisanje teksta i članaka"
  "LeetTradeBot AI bot za trading i finansijske operacije"
  "LeetCodeBot AI bot za generisanje koda i debugging"
  "LeetGeneralBot Generalni AI bot za chat i taskove"
)

echo "Pokretanje telegram-cli za login sa brojem: $TELEGRAM_PHONE"
echo "Slijedi upute za login (unesi kod iz Telegrama ako zatraži)."

# Pokreni telegram-cli u pozadini i loguj se
telegram-cli -k tg-server.pub -W -e "safe_quit" &
sleep 5  # Čekaj da se pokrene

# Pošalji /newbot BotFather-u za svaki bot
for BOT_INFO in "${BOTS[@]}"; do
  BOT_NAME=$(echo $BOT_INFO | cut -d' ' -f1)
  BOT_DESC=$(echo $BOT_INFO | cut -d' ' -f2-)
  
  echo "Kreiranje bota: $BOT_NAME sa opisom: $BOT_DESC"
  
  # Pošalji komande BotFather-u
  telegram-cli -k tg-server.pub -W -e "msg @BotFather /newbot"
  sleep 2
  telegram-cli -k tg-server.pub -W -e "msg @BotFather $BOT_NAME"
  sleep 2
  telegram-cli -k tg-server.pub -W -e "msg @BotFather $BOT_DESC"
  sleep 5  # Čekaj odgovor
  
  # Dohvati token iz poslednje poruke (pretpostavimo format "Use this token to access the HTTP API: <TOKEN>")
  TOKEN=$(telegram-cli -k tg-server.pub -W -e "history @BotFather 1" | grep "Use this token" | sed 's/.*Use this token to access the HTTP API: //')
  
  if [ -n "$TOKEN" ]; then
    echo "Token za $BOT_NAME: $TOKEN"
    # Dodaj u .env (u uppercase sa _BOT_TOKEN)
    UPPER_NAME=$(echo $BOT_NAME | tr 'a-z' 'A-Z' | sed 's/BOT$//')_BOT_TOKEN=$TOKEN
    echo $UPPER_NAME >> .env
    echo "Dodan u .env: $UPPER_NAME"
  else
    echo "Greška: Token za $BOT_NAME nije dohvaćen. Provjeri manuelno."
  fi
done

# Završi telegram-cli
telegram-cli -k tg-server.pub -W -e "safe_quit"

echo "Svi botovi kreirani. Provjeri .env fajl."
