import os
import time
import requests
from bs4 import BeautifulSoup

TOKEN = os.environ["TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
URL = os.environ["URL"]

seen = set()

def send(text):
    requests.get(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": text}
    )

def get_ads():
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    ads = []

    for a in soup.select('a[data-marker="item-title"]'):
        title = a.get_text(strip=True)
        link = a.get("href")

        if link and link.startswith("/"):
            link = "https://www.avito.ru" + link

        ads.append((title, link))

    return ads

send("✅ Авито монитор запущен")

while True:
    try:
        for title, link in get_ads():
            if link not in seen:
                seen.add(link)
                send(f"🔥 Новое объявление\n\n{title}\n{link}")

        time.sleep(40)

    except Exception as e:
        send(f"⚠️ Ошибка: {e}")
        time.sleep(60)
