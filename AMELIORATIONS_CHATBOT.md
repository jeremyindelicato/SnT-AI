# Plan d'Améliorations du Chatbot Start&Trade

## ✅ Succès Actuel
- ✅ Détection de tickers via mapping intelligent (60+ entreprises)
- ✅ MCP tool fonctionne correctement
- ✅ Données enrichies scrapées (capitalisation, P/E, volumes, etc.)
- ✅ Le modèle utilise maintenant les données injectées
- ✅ Timeout augmenté (2 minutes)
- ✅ Prompts renforcés pour forcer l'utilisation des données

---

## 🔴 Problèmes Critiques à Résoudre

### 1. **Prix Scrapé Incorrect** (URGENT)

**Problème** :
- Prix retourné : 8 344$ pour AAPL
- Prix réel : ~259$
- Cause : Yahoo Finance FR affiche 26 tickers sur la même page (CAC 40, LVMH, etc.)
- Le scraper prend le premier tag `regularMarketPrice` qui n'est PAS AAPL

**Solution 1 : Utiliser l'API Yahoo Finance** (RECOMMANDÉ)

Yahoo Finance a une API JSON non-officielle mais stable :
```
https://query1.finance.yahoo.com/v8/finance/chart/AAPL?interval=1d
```

**Avantages** :
- ✅ Données JSON structurées (pas de parsing HTML)
- ✅ Plus rapide (~200ms vs ~2s)
- ✅ Plus fiable (pas de changements HTML)
- ✅ Données en temps réel exactes

**Solution 2 : Scraping Ciblé**
Chercher le tag dans une section spécifique de la page (avec un ID ou une classe CSS unique pour AAPL).

**Solution 3 : Utiliser yfinance (bibliothèque Python)**
```bash
pip install yfinance
```
```python
import yfinance as yf
ticker = yf.Ticker("AAPL")
data = ticker.info  # Toutes les données
```

### 2. **Nom de l'Entreprise Incorrect**

**Problème** : Scraper retourne "Yahoo Finance" au lieu de "Apple Inc."

**Solution** : Chercher un autre sélecteur pour le nom :
```python
# Chercher dans les meta tags
name_tag = soup.find('meta', {'property': 'og:title'})
name = name_tag['content'].split('(')[0].strip() if name_tag else symbol
```

### 3. **Performance du Modèle (IMPORTANT)**

**Problème** : Phi 3.5 Mini (4k context) :
- Lent (60-90 secondes par requête)
- Hallucinations fréquentes (invente des données malgré les instructions)
- Répétitif et verbeux

**Solution** : Passer à un modèle plus performant

**Modèles Recommandés** :

| Modèle | Vitesse | Qualité | Taille | Commande |
|--------|---------|---------|--------|----------|
| **Qwen2.5:7b** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 4.7 GB | `ollama pull qwen2.5:7b` |
| Llama 3.1:8b | ⭐⭐ | ⭐⭐⭐⭐ | 4.7 GB | `ollama pull llama3.1:8b` |
| Mistral:7b | ⭐⭐⭐ | ⭐⭐⭐⭐ | 4.1 GB | `ollama pull mistral:7b` |
| Gemma2:9b | ⭐⭐ | ⭐⭐⭐⭐ | 5.4 GB | `ollama pull gemma2:9b` |

**Mon recommandation : Qwen2.5:7b**
- Excellent en suivant les instructions
- Très bon en français
- Rapide (~15-20s par requête)
- Excellent pour les tâches structurées

**Pour changer** :
1. Télécharger : `ollama pull qwen2.5:7b`
2. Modifier `backend/.env` : `OLLAMA_MODEL=qwen2.5:7b`
3. Relancer le backend

---

## 🟡 Améliorations Moyennes Priorité

### 4. **Ajout de Nouveaux Tools MCP**

**Tool 1 : Données Historiques**
```python
# backend/mcp/tools.py
def get_historical_data(ticker: str, period: str = "1mo"):
    """Récupère l'historique des prix (1j, 1sem, 1m, 1an)"""
    # Via API Yahoo Finance
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    params = {"interval": "1d", "range": period}
    # ...
```

**Tool 2 : Actualités**
```python
def get_news(ticker: str, limit: int = 5):
    """Récupère les 5 dernières news pour un ticker"""
    # Via Yahoo Finance RSS ou API
```

**Tool 3 : Comparaison de Tickers**
```python
def compare_tickers(tickers: list[str], metrics: list[str]):
    """Compare plusieurs actions (P/E, cap, dividend yield)"""
```

### 5. **Amélioration de l'Interface Frontend**

**Affichage Structuré** :
- Cartes pour les métriques importantes (prix, +/- jour, capitalisation)
- Graphique simple avec Chart.js
- Code couleur : vert (hausse), rouge (baisse)

**Exemple de design** :
```
┌─────────────────────────────────┐
│ 📊 Apple Inc. (AAPL)            │
├─────────────────────────────────┤
│ Prix actuel: 259.41$            │
│ Variation: -0.71$ (-0.27%) 🔴   │
│ Capitalisation: 3.8T$           │
│ P/E Ratio: 34.84                │
└─────────────────────────────────┘
```

### 6. **Gestion de la Conversation**

**Contexte Multi-Tours** :
- Permettre : "Comment va Apple ?" puis "Et Microsoft ?"
- Mémoriser les tickers mentionnés
- Comparaisons automatiques : "Compare les deux"

**Suggestions Intelligentes** :
```python
# Après avoir montré Apple
suggestions = [
    "Veux-tu voir les performances de Microsoft ?",
    "Souhaites-tu comparer Apple avec Google ?",
    "Veux-tu comprendre ce qu'est le ratio P/E ?"
]
```

### 7. **Éducation Interactive**

**Explications Contextuelles** :
- Détecter les termes financiers dans la réponse
- Ajouter des tooltips/popups explicatifs
- Glossaire intégré

**Exemples** :
- User : "C'est quoi le P/E ?"
- Bot : Explication avec exemple d'Apple vs Microsoft

### 8. **Cache des Données**

**Problème** : Scraper appelé à chaque question même pour le même ticker

**Solution** :
```python
# backend/app/cache.py
from datetime import datetime, timedelta

cache = {}

def get_cached_data(ticker: str, max_age_minutes: int = 5):
    if ticker in cache:
        data, timestamp = cache[ticker]
        if datetime.now() - timestamp < timedelta(minutes=max_age_minutes):
            return data
    return None

def set_cached_data(ticker: str, data: dict):
    cache[ticker] = (data, datetime.now())
```

---

## 🟢 Améliorations Faible Priorité (Nice-to-Have)

### 9. **Multi-Langue**

Supporter anglais en plus du français :
```python
# backend/app/prompts.py
def get_system_prompt(language: str = "fr"):
    if language == "en":
        return ENGLISH_SYSTEM_PROMPT
    return FRENCH_SYSTEM_PROMPT
```

### 10. **Alertes et Notifications**

Permettre de configurer des alertes :
- "Préviens-moi si Apple descend sous 250$"
- "Alerte si le volume dépasse 2x la moyenne"

### 11. **Export de Données**

Bouton pour exporter :
- PDF avec résumé de la conversation
- CSV avec les données financières affichées
- Graphiques PNG

### 12. **Watchlist**

Permettre de sauvegarder des tickers favoris :
```python
# Frontend
const watchlist = ["AAPL", "MSFT", "GOOGL", "MC.PA"]

// Afficher un dashboard avec tous les favoris
```

### 13. **Mode Sombre / Clair**

Toggle pour changer le thème (déjà premium avec gold, mais option de personnalisation).

### 14. **Voice Input**

Permettre de poser des questions à la voix :
```javascript
// Frontend
const recognition = new webkitSpeechRecognition();
recognition.lang = 'fr-FR';
recognition.onresult = (e) => {
  const transcript = e.results[0][0].transcript;
  sendMessage(transcript);
}
```

---

## 📋 Roadmap Recommandée

### Phase 1 : Corrections Critiques (1-2 jours)
1. ✅ Fix du contexte MCP (FAIT)
2. 🔴 Corriger le prix scrapé (API Yahoo Finance ou yfinance)
3. 🔴 Changer pour Qwen2.5:7b
4. 🟡 Corriger le nom de l'entreprise

### Phase 2 : Amélioration de la Qualité (3-5 jours)
5. 🟡 Cache des données (éviter re-scraping)
6. 🟡 Tool historique (graphiques de prix)
7. 🟡 Tool actualités
8. 🟡 Amélioration UI (cartes métriques)

### Phase 3 : Fonctionnalités Avancées (1-2 semaines)
9. 🟢 Comparaison de tickers
10. 🟢 Watchlist
11. 🟢 Éducation interactive (glossaire)
12. 🟢 Export PDF/CSV

### Phase 4 : Polish et Extensions (optionnel)
13. 🟢 Multi-langue
14. 🟢 Alertes
15. 🟢 Voice input
16. 🟢 Mode sombre/clair

---

## 🎯 Quick Wins (À Faire Aujourd'hui)

### 1. Installer et Tester Qwen2.5:7b (10 min)
```bash
ollama pull qwen2.5:7b
```

Modifier `backend/.env` :
```
OLLAMA_MODEL=qwen2.5:7b
```

Relancer et tester → Devrait être **beaucoup plus rapide et précis**

### 2. Installer yfinance pour Fix du Prix (5 min)
```bash
cd backend
source venv/bin/activate
pip install yfinance
```

Tester :
```python
import yfinance as yf
ticker = yf.Ticker("AAPL")
print(ticker.info['currentPrice'])  # Devrait afficher ~259
```

### 3. Créer un Script de Test Rapide (5 min)
```bash
# backend/test_quick.py
import yfinance as yf

tickers = ["AAPL", "MSFT", "GOOGL", "MC.PA", "AI.PA"]
for symbol in tickers:
    try:
        stock = yf.Ticker(symbol)
        price = stock.info.get('currentPrice', 'N/A')
        name = stock.info.get('longName', symbol)
        print(f"{symbol}: {name} = {price}$")
    except Exception as e:
        print(f"{symbol}: ERREUR - {e}")
```

Exécuter :
```bash
python test_quick.py
```

Si ça marche → Remplacer tout le scraping BeautifulSoup par yfinance.

---

## 💡 Recommandations Finales

### Court Terme (Cette Semaine)
1. **Passer à Qwen2.5:7b** → Qualité +50%, Vitesse x3
2. **Remplacer scraping par yfinance** → Prix corrects, plus rapide, plus simple
3. **Ajouter un cache** → Éviter d'appeler l'API 10x pour la même action

### Moyen Terme (2-3 Semaines)
4. **Ajouter tool historique** → Graphiques, tendances
5. **Améliorer l'UI** → Cartes, visuels, graphiques
6. **Tool actualités** → Context sur pourquoi une action monte/descend

### Long Terme (1-2 Mois)
7. **Comparaison multi-tickers** → "Compare Apple, Microsoft et Google"
8. **Watchlist + alertes** → Suivi personnalisé
9. **Éducation interactive** → Mini-cours intégrés

---

## 🚀 Commandes pour Commencer

```bash
# 1. Installer le meilleur modèle
ollama pull qwen2.5:7b

# 2. Installer yfinance
cd backend
source venv/bin/activate
pip install yfinance

# 3. Modifier .env
echo "OLLAMA_MODEL=qwen2.5:7b" >> .env

# 4. Relancer
python -m uvicorn app.main:app --reload --port 8000
```

Testez avec la même question et vous verrez une **ÉNORME amélioration** ! 🎉
