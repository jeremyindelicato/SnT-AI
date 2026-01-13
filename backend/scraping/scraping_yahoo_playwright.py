"""
Yahoo Finance Scraping Module using Playwright (navigateur headless)
Résout le problème de détection de bot de Yahoo Finance
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

        # Structure de base
        content = {
            "metadata": {
                "source": "Yahoo Finance (Playwright)",
                "timestamp": datetime.now().isoformat(),
            },
            "global_market": {},
            "details": {}
        }

        # Chargement de l'existant
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
                    if "global_market" in existing or "details" in existing:
                        content = existing
            except Exception:
                pass

        content["metadata"]["timestamp"] = datetime.now().isoformat()

        if section == "global":
            content["global_market"] = data
        elif section == "details":
            symbol = data.get("symbol")
            if symbol:
                content["details"][symbol] = data

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=4)

        logger.info(f"Données sauvegardées avec succès dans : {json_path}")

    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde JSON : {str(e)}")


def get_ticker_details_playwright(symbol: str):
    """
    Scrape detailed data for a specific ticker using Playwright.
    Résout le problème de détection de bot.
    """
    url = f"https://finance.yahoo.com/quote/{symbol}"

    try:
        logger.info(f"Scraping {symbol} from {url} with Playwright...")

        with sync_playwright() as p:
            # Lancer le navigateur headless
            browser = p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )

            # Créer une page avec user agent réaliste
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080}
            )
            page = context.new_page()

            # Aller sur la page
            page.goto(url, wait_until='domcontentloaded', timeout=60000)

            # Gérer la popup de cookies si elle apparaît
            try:
                # Yahoo a une popup "guce" pour les cookies
                reject_button = page.query_selector('button[name="reject"], .reject-all, [class*="reject"]')
                if reject_button:
                    logger.info("Rejecting cookie consent...")
                    reject_button.click()
                    page.wait_for_timeout(2000)
            except:
                pass

            # Attendre que les données se chargent
            try:
                page.wait_for_selector('fin-streamer[data-field="regularMarketPrice"]', timeout=15000)
            except:
                logger.warning(f"fin-streamer not found, trying to continue anyway...")
                page.wait_for_timeout(2000)

            # Extraire le nom (h1)
            name_elem = page.query_selector('h1')
            name = name_elem.text_content().strip() if name_elem else symbol

            # Fonction helper pour extraire les données fin-streamer
            def get_streamer_value(field: str) -> str:
                elem = page.query_selector(f'fin-streamer[data-field="{field}"]')
                if elem:
                    return elem.text_content().strip()
                return "N/A"

            # Extraire toutes les données importantes
            details = {}

            # Mapping des champs
            streamer_map = {
                # Prix et variations
                'regularMarketPrice': 'Prix actuel',
                'regularMarketChange': 'Variation',
                'regularMarketChangePercent': 'Variation %',
                'regularMarketOpen': 'Ouverture',
                'regularMarketDayHigh': 'Plus haut du jour',
                'regularMarketDayLow': 'Plus bas du jour',
                'regularMarketPreviousClose': 'Clôture précédente',
                'regularMarketDayRange': 'Plage du jour',

                # Volumes et plages
                'regularMarketVolume': 'Volume',
                'averageVolume': 'Volume moyen',
                'fiftyTwoWeekRange': 'Plage sur 52 semaines',
                'fiftyTwoWeekHigh': 'Plus haut 52 semaines',
                'fiftyTwoWeekLow': 'Plus bas 52 semaines',

                # Valorisation
                'marketCap': 'Capitalisation boursière',
                'trailingPE': 'Ratio C/B (P/E)',
                'forwardPE': 'Ratio C/B prévisionnel',
                'priceToBook': 'Ratio prix/valeur comptable',
                'enterpriseValue': 'Valeur d\'entreprise',

                # Performance et cibles
                'beta': 'Bêta (volatilité)',
                'targetMeanPrice': 'Prix cible moyen',
                'targetHighPrice': 'Prix cible haut',
                'targetLowPrice': 'Prix cible bas',

                # Dividendes
                'dividendYield': 'Rendement du dividende',
                'dividendRate': 'Dividende annuel',

                # Bénéfices
                'epsTrailingTwelveMonths': 'BPA (12 derniers mois)',
                'epsForward': 'BPA prévisionnel',
            }

            for field, label in streamer_map.items():
                value = get_streamer_value(field)
                if value and value != "N/A":
                    details[label] = value

            # Extraire aussi les données des tableaux
            tables = page.query_selector_all('table')
            for table in tables:
                rows = table.query_selector_all('tr')
                for row in rows:
                    cols = row.query_selector_all('td')
                    if len(cols) == 2:
                        key = cols[0].text_content().strip()
                        value = cols[1].text_content().strip()
                        if key and value:
                            details[key] = value

            # Construire l'objet de données
            price = details.get('Prix actuel', 'N/A')
            change = details.get('Variation', 'N/A')
            percent_change = details.get('Variation %', 'N/A')

            data = {
                "symbol": symbol,
                "name": name,
                "price": price,
                "change": change,
                "percent_change": percent_change,
                "details": details,
                "url": url,
                "source": "Yahoo Finance (Playwright)"
            }

            # Fermer le navigateur
            browser.close()

            # Sauvegarder
            save_data_to_json(data, section="details")

            logger.info(f"✅ Successfully scraped {symbol}: {price}")
            return data

    except PlaywrightTimeoutError:
        logger.error(f"Timeout scraping {symbol}")
        return {
            "error": f"Timeout lors du scraping de {symbol}",
            "symbol": symbol
        }
    except Exception as e:
        logger.error(f"Error scraping {symbol}: {str(e)}")
        return {
            "error": f"Failed to scrape {symbol}",
            "details": str(e),
            "symbol": symbol
        }


def get_market_data(symbol: str = None):
    """
    Main entry point for scraping.
    Uses Playwright for reliable data extraction.
    """
    if symbol:
        return get_ticker_details_playwright(symbol)

    # Si pas de symbol, retourner erreur
    return {"error": "Symbol required for Playwright scraping"}


if __name__ == "__main__":
    # Test
    import sys
    test_symbol = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    print(f"\n🧪 Testing Playwright scraper with {test_symbol}...\n")
    result = get_market_data(test_symbol)
    print(json.dumps(result, indent=2, ensure_ascii=False))
