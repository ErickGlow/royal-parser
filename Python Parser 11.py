import requests
from bs4 import BeautifulSoup
from datetime import datetime, UTC
import re

TARGET = "cryptoroyal"

PAIRS = {
    "UAH → USDT (TRC20)": "https://www.bestchange.com/visa-mastercard-uah-to-tether-trc20.html",
    "RUB → USDT (TRC20)": "https://www.bestchange.com/visa-mastercard-rub-to-tether-trc20.html",
    "USD → USDT (TRC20)": "https://www.bestchange.com/visa-mastercard-usd-to-tether-trc20.html",
    "EUR → USDT (TRC20)": "https://www.bestchange.com/visa-mastercard-eur-to-tether-trc20.html",
    "UAH → BTC": "https://www.bestchange.com/visa-mastercard-uah-to-bitcoin.html",
}


def clean(text):
    return re.sub(r"\s+", " ", text).strip()


def parse_pair(name, url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    r = requests.get(url, headers=headers, timeout=20)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    rows = soup.find_all("tr")

    position = 0

    for row in rows:
        text = row.get_text(" ", strip=True)
        if not text:
            continue

        # считаем только реальные стаканы
        if any(x in text for x in ["UAH", "RUB", "USD", "EUR"]) and any(
            x in text for x in ["USDT", "BTC"]
        ):
            position += 1

        if TARGET in text.lower():
            rate = re.search(r"\d+\.\d+\s*[A-Z]{3}", text)
            reserve = re.search(r"\d[\d\s]{5,}", text)

            print(f"📊 {name}")
            print(f"   🏦 CryptoRoyal: место #{position}")
            if rate:
                print(f"   💸 Курс: {rate.group(0)}")
            if reserve:
                print(f"   🏦 Резерв: {clean(reserve.group(0))}")
            return

    print(f"📊 {name}")
    print("   ❌ CryptoRoyal не участвует")


def main():
    print("✅ BestChange monitoring — реальные позиции CryptoRoyal\n")

    for name, url in PAIRS.items():
        try:
            parse_pair(name, url)
        except Exception as e:
            print(f"📊 {name}")
            print(f"   ⚠️ Ошибка: {e}")

    print(f"\n🕒 {datetime.now(UTC).isoformat()}")


if __name__ == "__main__":
    main()
