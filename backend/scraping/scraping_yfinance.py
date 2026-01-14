"""
Yahoo Finance Scraping Module using yfinance library
yfinance est une bibliothèque qui scrape Yahoo Finance de manière robuste
C'est toujours du scraping (pas d'API officielle), mais déguisé en bibliothèque
"""
import logging
import json
import os
from datetime import datetime
import yfinance as yf

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
                "source": "Yahoo Finance (yfinance)",
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


def format_number(value):
    """Format a number for display."""
    if value is None or (isinstance(value, float) and (value != value)):  # Check for NaN
        return "N/A"
    if isinstance(value, (int, float)):
        return f"{value:,.2f}"
    return str(value)


def get_ticker_details(symbol: str):
    """
    Récupère les données via yfinance (scraping robuste de Yahoo Finance).
    """
    try:
        logger.info(f"Fetching data for {symbol} using yfinance...")

        # Créer l'objet ticker
        ticker = yf.Ticker(symbol)

        # Récupérer les infos
        info = ticker.info

        if not info or 'symbol' not in info:
            logger.error(f"No data found for {symbol}")
            return {"error": f"Ticker {symbol} not found", "symbol": symbol}

        # Extraire les données principales
        name = info.get('longName', info.get('shortName', symbol))
        current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
        previous_close = info.get('previousClose', info.get('regularMarketPreviousClose', 0))

        # Calculer la variation
        if current_price and previous_close:
            change = current_price - previous_close
            percent_change = (change / previous_close) * 100
            change_str = f"{change:+.2f}"
            percent_str = f"({percent_change:+.2f}%)"
        else:
            change_str = "N/A"
            percent_str = "N/A"

        # Construire les détails
        details = {}

        # Prix et variations
        details["Prix actuel"] = format_number(current_price)
        details["Variation"] = change_str
        details["Variation %"] = percent_str
        details["Ouverture"] = format_number(info.get('open', info.get('regularMarketOpen')))
        details["Plus haut du jour"] = format_number(info.get('dayHigh', info.get('regularMarketDayHigh')))
        details["Plus bas du jour"] = format_number(info.get('dayLow', info.get('regularMarketDayLow')))
        details["Clôture précédente"] = format_number(previous_close)

        # Volumes
        volume = info.get('volume', info.get('regularMarketVolume'))
        avg_volume = info.get('averageVolume', info.get('averageDailyVolume10Day'))
        details["Volume"] = f"{volume:,}" if volume else "N/A"
        details["Volume moyen"] = f"{avg_volume:,}" if avg_volume else "N/A"

        # Plages
        fifty_two_low = info.get('fiftyTwoWeekLow')
        fifty_two_high = info.get('fiftyTwoWeekHigh')
        if fifty_two_low and fifty_two_high:
            details["Plage sur 52 semaines"] = f"{fifty_two_low:.2f} - {fifty_two_high:.2f}"

        # Valorisation
        market_cap = info.get('marketCap')
        if market_cap:
            if market_cap >= 1_000_000_000_000:
                details["Capitalisation boursière"] = f"{market_cap / 1_000_000_000_000:.2f}T"
            elif market_cap >= 1_000_000_000:
                details["Capitalisation boursière"] = f"{market_cap / 1_000_000_000:.2f}B"
            else:
                details["Capitalisation boursière"] = f"{market_cap / 1_000_000:.2f}M"

        details["Ratio C/B (P/E)"] = format_number(info.get('trailingPE'))
        details["Ratio C/B prévisionnel"] = format_number(info.get('forwardPE'))
        details["Ratio prix/valeur comptable"] = format_number(info.get('priceToBook'))

        # Performance
        details["Bêta (volatilité)"] = format_number(info.get('beta'))
        target_mean = info.get('targetMeanPrice')
        if target_mean:
            details["Prix cible moyen"] = f"{target_mean:.2f}"

        # Dividendes
        dividend_yield = info.get('dividendYield')
        if dividend_yield:
            details["Rendement du dividende"] = f"{dividend_yield * 100:.2f}%"

        dividend_rate = info.get('dividendRate')
        if dividend_rate:
            details["Dividende annuel"] = f"{dividend_rate:.2f}"

        # Bénéfices
        details["BPA (12 derniers mois)"] = format_number(info.get('trailingEps'))
        details["BPA prévisionnel"] = format_number(info.get('forwardEps'))
        details["Marge bénéficiaire"] = format_number(info.get('profitMargins'))
        details["Marge opérationnelle"] = format_number(info.get('operatingMargins'))

        # Santé financière
        details["Retour sur actifs (ROA)"] = format_number(info.get('returnOnAssets'))
        details["Retour sur capitaux propres (ROE)"] = format_number(info.get('returnOnEquity'))
        details["Ratio dette/capitaux propres"] = format_number(info.get('debtToEquity'))
        details["Ratio de liquidité"] = format_number(info.get('currentRatio'))

        # Construire l'objet de données
        data = {
            "symbol": symbol,
            "name": name,
            "price": format_number(current_price),
            "change": change_str,
            "percent_change": percent_str,
            "details": {k: v for k, v in details.items() if v != "N/A"},  # Filtrer les N/A
            "url": f"https://finance.yahoo.com/quote/{symbol}",
            "source": "Yahoo Finance (yfinance)"
        }

        save_data_to_json(data, section="details")

        logger.info(f"✅ Successfully fetched data for {symbol}: ${current_price:.2f}")
        return data

    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {str(e)}")
        return {
            "error": f"Failed to fetch data for {symbol}",
            "details": str(e),
            "symbol": symbol
        }


def get_market_data(symbol: str = None):
    """
    Main entry point for scraping.
    """
    if symbol:
        return get_ticker_details(symbol)

    return {"error": "Symbol required"}


if __name__ == "__main__":
    # Test
    import sys
    test_symbol = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    print(f"\n🧪 Testing yfinance scraper with {test_symbol}...\n")
    result = get_market_data(test_symbol)
    print(json.dumps(result, indent=2, ensure_ascii=False))
