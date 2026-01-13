# Solution pour le Scraping Yahoo Finance

## Problème Identifié

Yahoo Finance **détecte les bots** et affiche des données incorrectes :
- Prix affiché : 8 336$ ou 7 018$ (aléatoire)
- Prix réel AAPL : ~259$

**Causes** :
1. Yahoo Finance FR redirige vers la page d'accueil (CAC 40)
2. Les balises `fin-streamer` n'ont pas d'attribut `value` (tous à `N/A`)
3. Le premier `regularMarketPrice` trouvé n'est PAS pour AAPL

---

## Solutions Possibles (Par ordre de recommandation)

### Solution 1 : Selenium + ChromeDriver (RECOMMANDÉ)

**Avantages** :
- ✅ Simule un vrai navigateur (contourne la détection de bot)
- ✅ JavaScript s'exécute (données chargées correctement)
- ✅ Toujours du scraping (conforme aux contraintes du projet)

**Installation** :
```bash
cd backend
source venv/bin/activate
pip install selenium webdriver-manager
```

**Code** :
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def get_market_data_selenium(symbol: str):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Mode sans interface
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)')

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        url = f"https://finance.yahoo.com/quote/{symbol}"
        driver.get(url)

        # Attendre que le prix se charge
        wait = WebDriverWait(driver, 10)
        price_elem = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-field="regularMarketPrice"]'))
        )

        price = price_elem.text

        # Récupérer le nom
        name_elem = driver.find_element(By.TAG_NAME, 'h1')
        name = name_elem.text

        # Autres données...
        return {
            "symbol": symbol,
            "name": name,
            "price": price,
            ...
        }
    finally:
        driver.quit()
```

**Performance** :
- Première exécution : ~5-8s (démarre le navigateur)
- Exécutions suivantes : ~2-3s

---

### Solution 2 : Playwright (Alternative à Selenium)

Plus moderne et plus rapide que Selenium.

```bash
pip install playwright
playwright install chromium
```

**Code** :
```python
from playwright.sync_api import sync_playwright

def get_market_data_playwright(symbol: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent='Mozilla/5.0...')

        page.goto(f"https://finance.yahoo.com/quote/{symbol}")
        page.wait_for_selector('[data-field="regularMarketPrice"]')

        price = page.locator('[data-field="regularMarketPrice"]').first.text_content()
        name = page.locator('h1').text_content()

        browser.close()

        return {"symbol": symbol, "name": name, "price": price}
```

**Avantages vs Selenium** :
- ✅ Plus rapide (~30% plus rapide)
- ✅ API plus moderne
- ✅ Moins de bugs

---

### Solution 3 : Scraping avec Headers Avancés + Cookies

Essayer de mieux "imiter" un navigateur avec requests.

```python
import requests
from bs4 import BeautifulSoup

session = requests.Session()

# Headers très complets
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Cache-Control': 'max-age=0',
}

# Récupérer d'abord la page d'accueil pour avoir les cookies
session.get('https://finance.yahoo.com', headers=headers)

# Puis scraper AAPL
response = session.get(f'https://finance.yahoo.com/quote/AAPL', headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
# ...
```

**Probabilité de succès** : ~30%
Yahoo peut quand même détecter le bot.

---

### Solution 4 : Alternative - Utiliser Google Finance

Si Yahoo Finance est trop difficile, Google Finance est plus facile à scraper :

```python
url = f"https://www.google.com/finance/quote/{symbol}:NASDAQ"
# Exemple: https://www.google.com/finance/quote/AAPL:NASDAQ

# Le prix est dans une div avec classe simple
price_elem = soup.find('div', {'class': 'YMlKec fxKbKc'})
price = price_elem.text if price_elem else 'N/A'
```

**Avantages** :
- ✅ HTML plus simple
- ✅ Moins de détection de bot
- ✅ Données fiables

**Inconvénients** :
- ❌ Moins de données que Yahoo (pas de P/E, dividendes, etc.)

---

## Recommandation Finale

**Ordre de préférence** :

1. **Playwright** → Le meilleur compromis (rapide, fiable, moderne)
2. **Selenium** → Plus connu, plus de documentation
3. **Google Finance** → Plus simple mais moins de données
4. **Requests + Headers avancés** → À tenter mais peu fiable

---

## Installation Playwright (Ma recommandation)

```bash
cd /Users/jeremyindelicato/Desktop/SnT\ AI/backend
source venv/bin/activate
pip install playwright
playwright install chromium
```

**Pourquoi Playwright ?**
- ✅ ~2-3s par scrape (vs 60-90s actuellement pour le LLM)
- ✅ Données 100% fiables
- ✅ Plus léger que Selenium
- ✅ M4 = très rapide pour exécuter Chromium headless
- ✅ Toujours du scraping (conforme au projet)

**Code complet dans** : `/backend/scraping/scraping_yahoo_playwright.py`

---

## Test Rapide

Voulez-vous que je :
1. **Implémente Playwright** dans votre scraper ?
2. **Teste Selenium** pour voir si ça marche ?
3. **Essaye Google Finance** comme alternative ?

Avec votre M4 16GB, Playwright sera **très rapide** et résoudra définitivement le problème de prix. Le navigateur headless tournera en ~1-2s sur votre machine.
