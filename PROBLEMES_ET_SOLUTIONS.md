# Problèmes Identifiés et Solutions

## Résumé des Problèmes

D'après vos logs, j'ai identifié **3 problèmes critiques** :

### ❌ Problème 1 : Timeouts Intermittents
**Symptôme** : Messages 1 et 3 affichent "backend non lancé" alors qu'il est bien lancé
**Cause** : Le modèle Ollama prend parfois > 60 secondes à répondre (Phi 3.5 Mini est petit et lent)
**Impact** : 2 requêtes sur 3 échouent avec timeout

### ❌ Problème 2 : Le Modèle Ignore les Données Financières (CRITIQUE)
**Symptôme** : Le modèle répond avec des données inventées au lieu d'utiliser celles scrapées
**Exemple concret de vos logs** :
- **Données scrapées** : `Prix actuel : 8 358,76` (+ capitalisation, P/E, volumes)
- **Réponse du modèle** : "Apple se négocie aux alentours de 189.45$"
- Le modèle **invente** des chiffres au lieu d'utiliser les vraies données

**Cause** : Phi 3.5 Mini (4k context) est trop petit pour bien suivre les instructions complexes

### ⚠️ Problème 3 : Prix Scrapé Incorrect
**Symptôme** : Le scraper retourne `8 358,76` au lieu de ~259$ pour AAPL
**Cause** : Le scraper attrape probablement un indice (CAC 40 ou autre) au lieu du prix de l'action

---

## Solutions Appliquées

### ✅ Solution 1 : Augmentation du Timeout
**Fichier modifié** : `frontend/src/services/api.js`
```javascript
timeout: 120000, // 2 minutes (était 30s)
```
**Impact** : Réduit les erreurs de timeout

### ✅ Solution 2 : Prompt Système Renforcé
**Fichier modifié** : `backend/app/prompts.py`

**Avant** : Instructions subtiles
```
Tu dois INTÉGRER ces données de manière NATURELLE...
```

**Après** : Instructions **EXPLICITES et DIRECTIVES**
```
⚠️ RÈGLE ABSOLUE - LIS ATTENTIVEMENT ⚠️
Quand tu vois un message système avec "[DONNÉES FINANCIÈRES EN TEMPS RÉEL]",
tu DOIS OBLIGATOIREMENT utiliser UNIQUEMENT les données de ce message.

NE JAMAIS inventer ou deviner des prix.
❌ INTERDIT : "Apple se négocie aux alentours de 189.45$" (données inventées)
✅ CORRECT : Utiliser EXACTEMENT les données du message système
```

**Pourquoi** : Les petits modèles comme Phi 3.5 Mini ont besoin d'instructions **très directes**. Les formulations polies comme "Tu dois intégrer" sont trop faibles.

### ✅ Solution 3 : Debug Logs Améliorés
**Fichier modifié** : `backend/app/agent.py`

Ajout de logs pour diagnostiquer :
```python
logger.info(f"Sending {len(self.conversation_history)} messages to Ollama (~{total_chars} chars)")
logger.info(f"Latest system message (financial data): {last_system['content'][:300]}...")
```

Cela permet de voir **exactement** ce qui est envoyé à Ollama.

---

## Test Après Modifications

### Étape 1 : Relancer le Backend

**IMPORTANT** : Fermez (CTRL+C) et relancez le backend pour charger les nouveaux prompts :

```bash
# Terminal 1 - Fermer avec CTRL+C puis relancer
cd /Users/jeremyindelicato/Desktop/SnT\ AI/backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000
```

Le MCP server peut rester tel quel (Terminal 2).

### Étape 2 : Relancer le Frontend

Le frontend doit recharger le nouveau timeout :

```bash
# Terminal 4 - Fermer avec CTRL+C puis relancer
cd /Users/jeremyindelicato/Desktop/SnT\ AI/frontend
npm run dev
```

### Étape 3 : Test avec la Même Question

Posez **exactement** la même question dans le frontend :
```
"à quel prix est l'action apple ?"
```

### Étape 4 : Analyser les Nouveaux Logs

**Dans Terminal 1 (Backend), cherchez** :
```
INFO:app.agent:Ticker détecté via mapping: 'apple' → AAPL
INFO:app.agent:Sending X messages to Ollama (~Y chars)
INFO:app.agent:Latest system message (financial data): Yahoo Finance (AAPL)
Prix actuel : 8 358,76
Variation du jour : -3,33 ((-0,04 %))

📊 Marché aujourd'hui
  • Ouverture : 259,16
  ...
```

**Ce qu'on veut voir** :
- ✅ Le modèle doit utiliser "8 358,76" dans sa réponse (même si c'est incorrect)
- ✅ Le modèle doit mentionner la capitalisation, le P/E, etc.
- ✅ Pas de données inventées comme "189.45$"

---

## Problème Restant à Résoudre : Prix Incorrect

### Diagnostic

Vos logs montrent :
```
'price': '8\u202f358,76'
'Ouverture': '259,16'
```

C'est **incohérent** :
- Le "Prix actuel" est 8 358,76
- L'"Ouverture" est 259,16

**Hypothèse** : Le scraper attrape deux éléments différents :
1. Pour "Prix actuel" : Un indice boursier (probablement CAC 40 qui est à ~8300)
2. Pour "Ouverture" : Le vrai prix d'AAPL (~259$)

### Solution : Corriger le Scraper

Le problème est dans `scraping_yahoo.py` ligne 193 :

```python
price = details.get('Prix actuel', details.get('Fermer', 'N/A'))
```

Il prend `'Prix actuel'` qui correspond au champ `regularMarketPrice`, mais celui-ci scrape apparemment le mauvais élément.

**Test pour confirmer** :

```bash
cd /Users/jeremyindelicato/Desktop/SnT\ AI/backend
source venv/bin/activate
python3 << 'EOF'
import requests
from bs4 import BeautifulSoup

url = "https://fr.finance.yahoo.com/quote/AAPL"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Trouver TOUS les fin-streamer avec regularMarketPrice
price_tags = soup.find_all('fin-streamer', {'data-field': 'regularMarketPrice'})
print(f"Nombre de tags 'regularMarketPrice' trouvés : {len(price_tags)}")
for i, tag in enumerate(price_tags):
    print(f"\nTag {i+1}:")
    print(f"  Valeur : {tag.get('value', 'N/A')}")
    print(f"  Texte : {tag.text.strip()}")
    print(f"  Classes : {tag.get('class', [])}")
    print(f"  Parent : {tag.parent.name if tag.parent else 'N/A'}")
EOF
```

**Résultat attendu** : Vous verrez probablement **2 tags** :
1. Un pour le CAC 40 (8 358)
2. Un pour AAPL (259)

**Fix** : Modifier le scraper pour prendre le **bon** tag (probablement avec une classe CSS spécifique ou un parent spécifique).

---

## Tests de Validation

### Test 1 : Données Utilisées Correctement ✅
**Question** : "à quel prix est l'action apple ?"
**Résultat attendu** : Le modèle doit mentionner "8 358,76" (même si incorrect) et les autres métriques (capitalisation, P/E)

### Test 2 : Pas de Données Inventées ✅
**Résultat attendu** : Le modèle ne doit PLUS dire "189.45$" ou toute autre valeur inventée

### Test 3 : Timeout Résolu ✅
**Résultat attendu** : Les 3 requêtes doivent passer (timeout à 2min)

### Test 4 : Prix Correct (À FAIRE)
**Action** : Corriger le scraper pour attraper le bon prix
**Résultat attendu** : Prix ~259$ au lieu de 8 358$

---

## Recommandation : Changer de Modèle

**Phi 3.5 Mini (4k)** est trop petit pour ce cas d'usage. Il :
- Ignore souvent les instructions complexes
- Invente des données même quand on lui dit explicitement de ne pas le faire
- Est lent (60-90s par requête)

**Modèles recommandés** :

1. **Qwen2.5:7b** (MEILLEUR choix)
   ```bash
   ollama pull qwen2.5:7b
   ```
   - Très bon à suivre les instructions
   - Rapide (~10-20s)
   - Excellent pour les tâches structurées

2. **Llama 3.1:8b**
   ```bash
   ollama pull llama3.1:8b
   ```
   - Excellent en français
   - Suit bien les instructions
   - ~15-30s

3. **Mistral:7b**
   ```bash
   ollama pull mistral:7b
   ```
   - Créé par une boîte française
   - Excellent français
   - ~20-30s

**Pour changer le modèle** :
1. Télécharger avec `ollama pull`
2. Modifier `backend/.env` :
   ```
   OLLAMA_MODEL=qwen2.5:7b
   ```
3. Relancer le backend

---

## Ordre des Actions Recommandées

1. ✅ **Relancer backend + frontend** (pour charger les nouveaux prompts)
2. ✅ **Tester avec "à quel prix est l'action apple ?"**
3. ✅ **Vérifier que le modèle utilise les données scrapées** (même si incorrectes)
4. ⚠️ **Corriger le scraper** (prix correct)
5. 🚀 **Changer pour Qwen2.5:7b** (meilleure qualité de réponses)

---

## Logs à Surveiller

Après relance, dans **Terminal 1 (Backend)**, vous devriez voir :

```
INFO:app.agent:Ticker détecté via mapping: 'apple' → AAPL
INFO:app.agent:Calling MCP tool: get_market_data with parameters: {'ticker': 'AAPL'}
INFO:app.agent:MCP tool result: success=True
INFO:app.agent:Sending 3 messages to Ollama (~XXXX chars)
INFO:app.agent:Latest system message (financial data): Yahoo Finance (AAPL)
Prix actuel : 8 358,76
Variation du jour : -3,33 ((-0,04 %))

📊 Marché aujourd'hui
  • Ouverture : 259,16
  ...
```

**Le modèle devrait maintenant utiliser ces données dans sa réponse.**

Si le modèle invente encore des données après les modifications, c'est une **limitation du modèle Phi 3.5 Mini**, et il faudra absolument passer à Qwen2.5:7b ou Llama 3.1:8b.
