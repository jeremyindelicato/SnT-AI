"""
Yahoo Finance Scraping Module using Requests & BeautifulSoup
"""
import logging
import requests
import json
import time
import os
from datetime import datetime
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

def save_data_to_json(data, filename="market_data.json", section="details"):
    """
    Helper function to save data to the JSON file.
    """
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.dirname(current_dir)
        data_dir = os.path.join(backend_dir, "data")
        os.makedirs(data_dir, exist_ok=True)
        
        json_path = os.path.join(data_dir, filename)
        
        # Structure de base pour accumuler les données
        content = {
            "metadata": {
                "source": "Yahoo Finance",
                "timestamp": datetime.now().isoformat(),
            },
            "global_market": {},
            "details": {}
        }
        
        # Chargement de l'existant pour ne pas écraser l'autre section
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

def get_session():
    """
    Creates a requests Session with retry logic for robust scraping.
    """
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1, # Attendre 1s, 2s, 4s entre les essais
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def get_ticker_details(symbol: str, session=None):
    """
    Scrapes detailed data for a specific ticker from Yahoo Finance.
    Target: https://fr.finance.yahoo.com/quote/ALIBR.PA
    """
    url = f"https://fr.finance.yahoo.com/quote/{symbol}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    # Utilisation de la session passée ou création d'une nouvelle
    if session is None:
        session = get_session()

    try:
        logger.info(f"Scraping details for {symbol} from {url}")
        response = session.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Basic Info
        name_tag = soup.find('h1')
        name = name_tag.text.strip() if name_tag else symbol
        
        # --- Extraction des indicateurs principaux (En-tête) ---
        # Mapping des champs fin-streamer vers les noms demandés
        streamer_map = {
            'regularMarketTime': 'Date',
            'regularMarketPrice': 'Fermer',
            'regularMarketOpen': 'Ouverture',
            'regularMarketDayHigh': 'Maximum',
            'regularMarketDayLow': 'Minimum',
            'regularMarketVolume': 'Volume'
        }
        
        details = {}
        
        for field, label in streamer_map.items():
            tag = soup.find('fin-streamer', {'data-field': field})
            if tag:
                # Traitement spécial pour la date (timestamp -> lisible)
                if field == 'regularMarketTime':
                    try:
                        ts = int(tag.get('value'))
                        details[label] = datetime.fromtimestamp(ts).strftime('%d/%m %I:%M %p')
                    except:
                        details[label] = tag.text.strip()
                else:
                    details[label] = tag.text.strip()
            else:
                details[label] = "n/a"

        # Récupération des variables classiques pour l'affichage résumé
        price = details.get('Fermer', 'N/A')
        # Pour le change et percent_change, on les prend aussi
        change_tag = soup.find('fin-streamer', {'data-field': 'regularMarketChange'})
        change = change_tag.text.strip() if change_tag else "N/A"
        pct_change_tag = soup.find('fin-streamer', {'data-field': 'regularMarketChangePercent'})
        percent_change = pct_change_tag.text.strip() if pct_change_tag else "N/A"
        
        # --- Extraction des données détaillées (Tableaux) ---
        # On cherche tous les tableaux car la structure peut varier (quote-summary, etc.)
        tables = soup.find_all('table')
        
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) == 2:
                    key = cols[0].text.strip()
                    value = cols[1].text.strip()
                    # On évite d'écraser les données streamer si elles sont déjà présentes et valides
                    # sauf si c'est pour avoir le libellé exact du tableau (ex: "Ouverture" vs "Ouverture")
                    # Ici on ajoute tout au dictionnaire details
                    details[key] = value
        
        # Construction de l'objet de données complet
        data = {
            "symbol": symbol,
            "name": name,
            "price": price,
            "change": change,
            "percent_change": percent_change,
            "details": details,
            "url": url,
            "source": "Yahoo Finance (Detail)"
        }
        
        # Sauvegarde immédiate dans le JSON pour inspection
        save_data_to_json(data, section="details")
        
        return data
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            logger.warning(f"Ticker {symbol} introuvable (404).")
            return {"error": "Ticker not found", "symbol": symbol}
        logger.error(f"HTTP Error scraping details for {symbol}: {str(e)}")
    except Exception as e:
        logger.error(f"Error scraping details for {symbol}: {str(e)}")
        return {"error": f"Failed to scrape details for {symbol}", "details": str(e)}

def get_market_data(symbol: str = None):
    """
    Scrapes currency data from Yahoo Finance using Requests.
    Target: https://fr.finance.yahoo.com/march%c3%a9s/actions/plus-liquides/
    
    Args:
        symbol (str): Optional ticker to filter the list.
        
    Returns:
        dict: List of currencies or specific currency data.
    """
    session = get_session()

    # If a specific ticker is requested, we go to the detail page directly
    if symbol:
        return get_ticker_details(symbol, session=session)

    url = "https://fr.finance.yahoo.com/march%c3%a9s/actions/plus-liquides/"
    # Headers pour simuler un navigateur réel et éviter les blocages
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    try:
        logger.info(f"Scraping {url} with requests")
        response = session.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        
        if not table:
            return {"error": "Tableau introuvable sur la page Yahoo Finance"}

        data = []
        # Extraction des lignes du tableau
        rows = table.find('tbody').find_all('tr')
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 5:
                item = {
                    "symbol": cols[0].text.strip(),
                    "name": cols[1].text.strip(),
                    "price": cols[2].text.strip(),
                    "change": cols[3].text.strip(),
                    "percent_change": cols[4].text.strip(),
                    "source": "Yahoo Finance (Requests)"
                }
                data.append(item)
        
        # Sauvegarde de la liste globale
        save_data_to_json({"items": data, "count": len(data)}, section="global")
        
        # Récupération des détails pour chaque action trouvée
        logger.info(f"Récupération des détails pour {len(data)} actions...")
        for item in data:
            sym = item.get('symbol')
            if sym:
                get_ticker_details(sym, session=session)
                time.sleep(0.5) # Pause réduite car la session réutilisée est plus efficace
        
        return {"currencies": data}

    except Exception as e:
        logger.error(f"Requests error: {str(e)}")
        return {
            "error": "Failed to scrape data",
            "details": str(e)
        }

if __name__ == "__main__":
    # Test : Récupère toutes les devises
    print(get_market_data())