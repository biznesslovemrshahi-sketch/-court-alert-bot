import requests, hashlib, json
from bs4 import BeautifulSoup

BOT_TOKEN = "8953619881:AAE88e-Vec7s8irvSRXSfB98ptp2zRXA1SA"
CHAT_ID = "6887445420"

COURTS = {
    "सर्वोच्च अदालत": "https://supremecourt.gov.np/cp/notices",
    "विशेष अदालत": "https://specialcourt.gov.np/en/notices",
    "उच्च अदालत पाटन": "https://phtc.p5.gov.np/en/notices-and-announcements",
    "प्रशासनिक अदालत": "https://supremecourt.gov.np/web/ac/notices",
    "राजस्व न्यायाधिकरण": "https://supremecourt.gov.np/web/rt-kathmandu/notices"
}

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown", "disable_web_page_preview": False}
    r = requests.post(url, data=data)
    print(r.text)

def check():
    try:
        with open("last.json","r") as f: old=json.load(f)
    except: old={}

    for name, link in COURTS.items():
        try:
            print(f"Checking {name}...")
            res = requests.get(link, timeout=30, headers={"User-Agent":"Mozilla/5.0"})
            soup = BeautifulSoup(res.text, 'html.parser')
            # सबै text को hash लिने
            text = soup.get_text(" ", strip=True)[:4000]
            h = hashlib.md5(text.encode()).hexdigest()

            if name not in old:
                old[name]=h
                print(f"{name} - First save")
            elif old[name]!=h:
                print(f"🔔 NEW in {name}")
                msg = f"🔔 *{name} मा नयाँ सूचना आयो!*\n\n🏛️ अदालत: {name}\n🔗 [नोटिस हेर्न क्लिक गर्नुहोस्]({link})\n\n⏰ {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}"
                send_telegram(msg)
                old[name]=h
            else:
                print(f"{name} - No change")
        except Exception as e:
            print(f"Error {name}: {e}")

    with open("last.json","w") as f: json.dump(old,f, indent=2)

check()
