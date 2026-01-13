"""
Google Finance Scraping Module using Playwright
Alternative plus simple à Yahoo Finance (pas de popup cookies)
"""
import logging
import json
import os
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

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
                "source": "Google Finance (Playwright)",
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


def get_ticker_details_google(symbol: str):
    """
    Scrape data from Google Finance - beaucoup plus simple que Yahoo.
    """
    # Google Finance nécessite le marché (NASDAQ, NYSE, EPA pour Paris, etc.)
    # Par défaut, essayer NASDAQ pour les US et EPA pour les actions françaises
    markets_to_try = []

    if symbol.endswith('.PA'):
        # Action française
        clean_symbol = symbol.replace('.PA', '')
        markets_to_try = [('EPA', clean_symbol), ('NASDAQ', symbol)]
    else:
        # Action US
        markets_to_try = [('NASDAQ', symbol), ('NYSE', symbol)]

    for market, clean_sym in markets_to_try:
        url = f"https://www.google.com/finance/quote/{clean_sym}:{market}"

        try:
            logger.info(f"Trying Google Finance: {url}")

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page(
                    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                )

                page.goto(url, timeout=30000)
                page.wait_for_timeout(2000)  # Attendre le chargement

                # Le prix est dans une div avec classe spécifique
                price_elem = page.query_selector('div.YMlKec.fxKbKc')
                if not price_elem:
                    logger.warning(f"Prix non trouvé pour {market}:{clean_sym}")
                    browser.close()
                    continue

                price = price_elem.text_content().strip()

                # Nom de l'entreprise
                name_elem = page.query_selector('div.zzDege')
                name = name_elem.text_content().strip() if name_elem else symbol

                # Variation
                change_elem = page.query_selector('div.JwB6zf span')
                change = change_elem.text_content().strip() if change_elem else "N/A"

                # Variation %
                percent_elem = page.query_selector('div.JwB6zf div[jsname] span')
                percent_change = percent_elem.text_content().strip() if percent_elem else "N/A"

                # Extraire les détails du tableau
                details = {}
                details["Prix actuel"] = price
                details["Variation"] = change
                details["Variation %"] = percent_change

                # Google Finance a des divs avec les stats
                stat_divs = page.query_selector_all('div.P6K39c')
                for stat_div in stat_divs:
                    label_elem = stat_div.query_selector('div.mfs7Fc')
                    value_elem = stat_div.query_selector('div.P6K39c')

                    if label_elem and value_elem:
                        label = label_elem.text_content().strip()
                        value = value_elem.text_content().strip()

                        # Mapping français
                        label_map = {
                            "Previous close": "Clôture précédente",
                            "Day range": "Plage du jour",
                            "Year range": "Plage sur 52 semaines",
                            "Market cap": "Capitalisation boursière",
                            "P/E ratio": "Ratio C/B (P/E)",
                            "Dividend yield": "Rendement du dividende",
                            "Volume": "Volume",
                            "Avg volume": "Volume moyen",
                        }

                        french_label = label_map.get(label, label)
                        details[french_label] = value

                browser.close()

                data = {
                    "symbol": symbol,
                    "name": name,
                    "price": price,
                    "change": change,
                    "percent_change": percent_change,
                    "details": details,
                    "url": url,
                    "source": "Google Finance (Playwright)"
                }

                save_data_to_json(data, section="details")
                logger.info(f"✅ Successfully scraped {symbol} from Google Finance: {price}")
                return data

        except Exception as e:
            logger.warning(f"Failed to scrape {market}:{clean_sym} - {str(e)}")
            continue

    # Aucun marché n'a fonctionné
    logger.error(f"Could not scrape {symbol} from any market")
    return {
        "error": f"Unable to find {symbol} on Google Finance",
        "symbol": symbol
    }


def get_market_data(symbol: str = None):
    """Main entry point"""
    if symbol:
        return get_ticker_details_google(symbol)

    return {"error": "Symbol required"}


if __name__ == "__main__":
    import sys
    test_symbol = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    print(f"\n🧪 Testing Google Finance scraper with {test_symbol}...\n")
    result = get_market_data(test_symbol)
    print(json.dumps(result, indent=2, ensure_ascii=False))
