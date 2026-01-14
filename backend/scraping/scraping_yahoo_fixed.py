"""
Yahoo Finance Scraping - Version Améliorée
Utilise des headers réalistes et scrape depuis l'URL anglaise (plus stable)
"""
import logging
import requests
import json
import time
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

def save_data_to_json(data, filename="market_data.json", section="details"):
    """Helper function to save data to the JSON file."""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.dirname(current_dir)
        data_dir = os.path.join(backend_dir, "data")
        os.makedirs(data_dir, exist_ok=True)

        json_path = os.path.join(data_dir, filename)

        content = {
            "metadata": {
                "source": "Yahoo Finance",
                "timestamp": datetime.now().isoformat(),
            },
            "global_market": {},
            "details": {}
        }

        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
                    if "global_market" in existing or "details" in existing:
                        content = existing
            except Exception:
                pass

        content["metadata"]["timestamp"] = datetime.now().isoformat()

        if section == "details":
            symbol = data.get("symbol")
            if symbol:
                content["details"][symbol] = data

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=4)

        logger.info(f"Données sauvegardées avec succès dans : {json_path}")

    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde JSON : {str(e)}")

def get_session():
    """Creates a requests Session with realistic headers and retry logic."""
    session = requests.Session()

    # Headers très complets pour imiter un vrai navigateur
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0',
    })

    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    return session

def extract_json_data(soup, symbol):
    """
    Extrait les données depuis le JSON embarqué dans les scripts.
    Yahoo Finance met les vraies données dans root.App.main
    """
    scripts = soup.find_all('script')

    for script in scripts:
        if script.string and 'root.App.main' in script.string:
            try:
                # Extraire le JSON
                match = re.search(r'root\.App\.main\s*=\s*(\{.*?\})\s*;', script.string, re.DOTALL)
                if not match:
                    continue

                json_str = match.group(1)
                data = json.loads(json_str)

                # Naviguer dans la structure
                quote_data = data['context']['dispatcher']['stores']['QuoteSummaryStore']
                price_data = quote_data.get('price', {})
                summary_data = quote_data.get('summaryDetail', {})

                # Extraire toutes les données
                result = {
                    'name': price_data.get('longName', symbol),
                    'price': price_data.get('regularMarketPrice', {}).get('fmt', 'N/A'),
                    'change': price_data.get('regularMarketChange', {}).get('fmt', 'N/A'),
                    'percent_change': price_data.get('regularMarketChangePercent', {}).get('fmt', 'N/A'),
                    'details': {}
                }

                # Détails du prix
                if 'regularMarketOpen' in price_data:
                    result['details']['Ouverture'] = price_data['regularMarketOpen'].get('fmt', 'N/A')
                if 'regularMarketDayHigh' in price_data:
                    result['details']['Plus haut du jour'] = price_data['regularMarketDayHigh'].get('fmt', 'N/A')
                if 'regularMarketDayLow' in price_data:
                    result['details']['Plus bas du jour'] = price_data['regularMarketDayLow'].get('fmt', 'N/A')
                if 'regularMarketPreviousClose' in price_data:
                    result['details']['Clôture précédente'] = price_data['regularMarketPreviousClose'].get('fmt', 'N/A')
                if 'marketCap' in price_data:
                    result['details']['Capitalisation boursière'] = price_data['marketCap'].get('fmt', 'N/A')

                # Détails du sommaire
                if 'volume' in summary_data:
                    result['details']['Volume'] = summary_data['volume'].get('fmt', 'N/A')
                if 'averageVolume' in summary_data:
                    result['details']['Volume moyen'] = summary_data['averageVolume'].get('fmt', 'N/A')
                if 'trailingPE' in summary_data:
                    result['details']['Ratio C/B (P/E)'] = summary_data['trailingPE'].get('fmt', 'N/A')
                if 'fiftyTwoWeekRange' in summary_data:
                    result['details']['Plage sur 52 semaines'] = summary_data['fiftyTwoWeekRange'].get('fmt', 'N/A')
                if 'dividendYield' in summary_data:
                    result['details']['Rendement du dividende'] = summary_data['dividendYield'].get('fmt', 'N/A')
                if 'beta' in summary_data:
                    result['details']['Bêta (volatilité)'] = summary_data['beta'].get('fmt', 'N/A')

                logger.info(f"✅ Données extraites depuis JSON embarqué: {result['price']}")
                return result

            except Exception as e:
                logger.warning(f"Erreur extraction JSON: {str(e)}")
                continue

    return None

def get_ticker_details(symbol: str, session=None):
    """
    Scrapes detailed data for a specific ticker from Yahoo Finance.
    Utilise l'URL anglaise (plus stable) et extrait depuis le JSON embarqué.
    """
    # Utiliser la version US de Yahoo Finance (plus stable)
    url = f"https://finance.yahoo.com/quote/{symbol}"

    if session is None:
        session = get_session()

    try:
        logger.info(f"Scraping {symbol} from {url}")

        # Petit délai pour éviter d'être détecté comme bot
        time.sleep(0.5)

        response = session.get(url, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Méthode 1 : Extraire depuis le JSON embarqué (MEILLEURE)
        json_data = extract_json_data(soup, symbol)

        if json_data:
            data = {
                "symbol": symbol,
                "name": json_data['name'],
                "price": json_data['price'],
                "change": json_data['change'],
                "percent_change": json_data['percent_change'],
                "details": json_data['details'],
                "url": url,
                "source": "Yahoo Finance (JSON Extract)"
            }

            save_data_to_json(data, section="details")
            return data

        # Méthode 2 : Fallback sur le scraping HTML classique
        logger.warning(f"JSON extraction failed for {symbol}, trying HTML parsing...")

        # Chercher le h1 pour le nom
        h1 = soup.find('h1')
        name = h1.text.strip() if h1 else symbol

        # Chercher le PREMIER fin-streamer après le h1
        price_elem = soup.find('fin-streamer', {'data-field': 'regularMarketPrice'})
        price = price_elem.text.strip() if price_elem else "N/A"

        change_elem = soup.find('fin-streamer', {'data-field': 'regularMarketChange'})
        change = change_elem.text.strip() if change_elem else "N/A"

        pct_elem = soup.find('fin-streamer', {'data-field': 'regularMarketChangePercent'})
        percent_change = pct_elem.text.strip() if pct_elem else "N/A"

        # Extraire les détails des tableaux
        details = {}
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) == 2:
                    key = cols[0].text.strip()
                    value = cols[1].text.strip()
                    if key and value:
                        details[key] = value

        data = {
            "symbol": symbol,
            "name": name,
            "price": price,
            "change": change,
            "percent_change": percent_change,
            "details": details,
            "url": url,
            "source": "Yahoo Finance (HTML Fallback)"
        }

        save_data_to_json(data, section="details")
        return data

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            logger.warning(f"Ticker {symbol} introuvable (404).")
            return {"error": "Ticker not found", "symbol": symbol}
        logger.error(f"HTTP Error scraping {symbol}: {str(e)}")
        return {"error": f"HTTP Error: {str(e)}", "symbol": symbol}
    except Exception as e:
        logger.error(f"Error scraping {symbol}: {str(e)}")
        return {"error": f"Failed to scrape {symbol}", "details": str(e), "symbol": symbol}

def get_market_data(symbol: str = None):
    """
    Main entry point for scraping.
    """
    session = get_session()

    if symbol:
        return get_ticker_details(symbol, session=session)

    return {"error": "Symbol required"}

if __name__ == "__main__":
    # Test
    import sys
    test_symbol = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    print(f"\n🧪 Testing improved scraper with {test_symbol}...\n")
    result = get_market_data(test_symbol)
    print(json.dumps(result, indent=2, ensure_ascii=False))
