# Guide de Test - Start&Trade

## Correction de l'Erreur MCP Server

### Problème
L'erreur `ERROR: Error loading ASGI app. Attribute "app" not found in module "mcp.mcp_server"` se produit car le serveur MCP exporte `mcp_app` et non `app`.

### Solution
Utilisez cette commande pour lancer le MCP server :

```bash
cd backend
source venv/bin/activate
python -m uvicorn mcp.mcp_server:mcp_app --reload --port 8001
```

---

## Procédure de Test Complète

### Étape 1 : Lancer tous les services

**Terminal 1 - Backend Principal (port 8000)**
```bash
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - MCP Server (port 8001)**
```bash
cd backend
source venv/bin/activate
python -m uvicorn mcp.mcp_server:mcp_app --reload --port 8001
```

**Terminal 3 - Ollama**
```bash
# Vérifier que le modèle est bien disponible
ollama list | grep phi3.5

# Si le modèle n'est pas présent :
ollama pull rouge/phi-3.5-mini-4k-instruct:latest

# Ollama devrait déjà être lancé en arrière-plan
# Si besoin, lancer : ollama serve
```

**Terminal 4 - Frontend**
```bash
cd frontend
npm run dev
```

### Étape 2 : Vérifier les health checks

**Backend Principal**
```bash
curl http://localhost:8000/health
# Devrait retourner : {"status":"healthy"}
```

**MCP Server**
```bash
curl http://localhost:8001/health
# Devrait retourner : {"status":"ok","message":"MCP Server is running"}
```

### Étape 3 : Test unitaire du MCP tool

```bash
curl -X POST http://localhost:8001/tools/execute \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "get_market_data", "parameters": {"ticker": "AAPL"}}'
```

**Résultat attendu :**
```json
{
  "success": true,
  "result": {
    "success": true,
    "context": "Apple Inc. (AAPL)\nCours actuel : 189.45\n...",
    "raw_data": {...}
  },
  "tool_name": "get_market_data"
}
```

### Étape 4 : Tests de détection de ticker

**Test 1 : Nom d'entreprise en français**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Comment va Apple actuellement sur la bourse ?"}'
```

**Logs attendus dans Terminal 1 (Backend) :**
```
INFO:app.agent:Ticker détecté dans le message: AAPL
INFO:app.agent:Ticker détecté via mapping: 'apple' → AAPL
INFO:app.agent:Calling MCP tool: get_market_data with parameters: {'ticker': 'AAPL'}
INFO:app.agent:MCP tool result: success=True
INFO:app.agent:Résultat MCP brut: {'success': True, 'context': '...', 'raw_data': {...}}
INFO:app.agent:Contexte financier injecté pour AAPL
```

**Test 2 : Ticker direct**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Donne-moi des infos sur MSFT"}'
```

**Test 3 : Entreprise française**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Quel est le cours de l'\''Oréal ?"}'
```
Devrait détecter : `OR.PA`

**Test 4 : Ticker invalide**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Donne-moi des infos sur INVALIDTICKER"}'
```

### Étape 5 : Test via le Frontend

1. Ouvrir http://localhost:5173 dans le navigateur
2. Taper : "Salut, je suis un jeune investisseur. Comment va Apple actuellement ?"
3. Vérifier que la réponse contient :
   - Le nom complet (Apple Inc.)
   - Le ticker (AAPL)
   - Le prix actuel
   - La variation du jour
   - Un contexte pédagogique

**Exemple de réponse attendue :**
```
Bonjour ! Ravi d'accompagner un jeune investisseur comme toi.

Apple (AAPL) se négocie actuellement à 189.45$, en hausse de 2.15$ (+1.14%) aujourd'hui.
C'est une belle performance ! Apple continue de montrer sa solidité sur le marché tech.

La capitalisation boursière est de 2.85T$, ce qui en fait l'une des entreprises les plus
valorisées au monde. Le volume d'échanges aujourd'hui est de 52.3M actions, ce qui montre
un bon niveau de liquidité.

Es-tu intéressé par comprendre ce qui influence ces variations de prix ?
```

---

## Diagnostic des Problèmes

### Problème : Le MCP server ne démarre pas
**Symptôme :** `ERROR: Error loading ASGI app`
**Solution :** Vérifier que vous utilisez `mcp_app` et non `app` dans la commande uvicorn

### Problème : Données vides dans la réponse
**Symptômes possibles :**
1. La réponse mentionne "[DONNÉES FINANCIÈRES EN TEMPS RÉEL]" mais sans données
2. Le modèle donne une réponse générique

**Diagnostic :**

1. **Vérifier les logs du Backend (Terminal 1)**
   - Chercher : `Ticker détecté dans le message`
   - Si absent → problème de détection de ticker
   - Si présent → continuer

2. **Vérifier l'appel MCP**
   - Chercher : `Calling MCP tool: get_market_data`
   - Chercher : `Résultat MCP brut:`
   - Si `success: False` → problème MCP

3. **Vérifier les logs du MCP Server (Terminal 2)**
   - Chercher : `[MCP TOOL CALL] get_market_data invoked for ticker: AAPL`
   - Chercher : `Scraping Yahoo Finance for AAPL...`
   - Chercher : `Successfully scraped data for AAPL`
   - Si erreurs → problème de scraping

4. **Vérifier l'injection de contexte**
   - Chercher : `Contexte financier injecté pour AAPL`
   - Si absent → le contexte n'est pas ajouté à l'historique

5. **Activer les logs DEBUG**
   ```python
   # Dans backend/app/main.py
   logging.basicConfig(level=logging.DEBUG)
   ```

### Problème : MCP server offline
**Symptôme :** `Le serveur MCP n'est pas disponible`
**Solution :** Vérifier que le Terminal 2 avec le MCP server est bien actif sur le port 8001

### Problème : Ticker non détecté
**Symptômes :** Aucun log "Ticker détecté" pour une question sur Apple
**Solutions :**
1. Vérifier que le mapping existe dans `TICKER_MAPPINGS`
2. Ajouter des logs dans `_extract_ticker()`
3. Tester avec un ticker explicite (AAPL) pour isoler le problème

---

## Tests Exhaustifs de Détection

### Entreprises US (via mapping)
- "Comment va Apple ?" → AAPL
- "Parle-moi de Microsoft" → MSFT
- "Infos sur Google" → GOOGL
- "Tesla actualités" → TSLA
- "Meta performance" → META
- "Nvidia cours" → NVDA

### Entreprises Françaises (via mapping)
- "Air Liquide prix" → AI.PA
- "LVMH cours" → MC.PA
- "L'Oréal bourse" → OR.PA
- "Total Energies" → TTE.PA
- "BNP Paribas action" → BNP.PA
- "Sanofi investissement" → SAN.PA

### Tickers directs (via regex)
- "Infos sur AAPL" → AAPL
- "Cours de MSFT" → MSFT
- "Performance AI.PA" → AI.PA

### Faux positifs (ne doivent PAS déclencher)
- "Qu'est-ce qu'un ETF ?" → aucun ticker
- "Parle-moi de l'IA en finance" → aucun ticker
- "CEO de quelle entreprise ?" → aucun ticker
- "IPO récentes USA" → aucun ticker

---

## Fichiers de Logs

Les logs importants se trouvent dans :
- Terminal 1 : Backend principal (agent.py, main.py)
- Terminal 2 : MCP server (mcp_server.py, tools.py)
- `backend/data/market_data.json` : Données scraped sauvegardées

---

## Commandes de Nettoyage

```bash
# Réinitialiser les données scraped
rm backend/data/market_data.json

# Réinstaller les dépendances
cd backend
pip install -r requirements.txt

# Vérifier les dépendances
pip list | grep -E "httpx|beautifulsoup4|ollama|fastapi"
```

---

## Checklist de Déploiement

- [ ] Tous les services démarrent sans erreur
- [ ] Les health checks répondent correctement
- [ ] Le test unitaire MCP tool fonctionne
- [ ] La détection de ticker fonctionne (logs visibles)
- [ ] Les données sont scraped correctement (JSON sauvegardé)
- [ ] Le contexte est injecté dans l'historique Ollama
- [ ] La réponse du modèle contient les données réelles
- [ ] Le style conversationnel fonctionne (pas de JSON brut)
- [ ] Les erreurs sont gérées proprement (ticker invalide, MCP offline)
- [ ] Le frontend affiche correctement les réponses
