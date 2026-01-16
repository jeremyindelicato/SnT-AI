# Start&Trade - Assistant Financier Intelligent

Un assistant conversationnel propulsé par l'IA locale pour accompagner les jeunes investisseurs dans leurs premiers pas sur les marchés financiers.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)
![Ollama](https://img.shields.io/badge/ollama-qwen2.5:7b-green.svg)

## À propos

Start&Trade est un chatbot financier pédagogique qui fonctionne entièrement en local sur votre machine. Le projet combine :

- Un moteur d'IA local (Qwen2.5:7b via Ollama) pour le raisonnement
- Du scraping en temps réel pour récupérer les données de marché
- Une base de connaissances structurée avec des concepts financiers
- Un système de routage intelligent qui détermine automatiquement quelle stratégie utiliser

### Objectifs du projet

Le projet vise à rendre l'analyse financière accessible aux débutants en combinant des données temps réel avec du contenu éducatif, le tout sans nécessiter d'API payantes ou de connexion internet permanente.

## Architecture

Le système suit une architecture multi-couches avec un routeur intelligent au centre :

```
┌─────────────────┐
│   Frontend      │  React + Vite + Tailwind
│   (Interface)   │  Design glassmorphism
└────────┬────────┘
         │ HTTP REST
         ↓
┌─────────────────────────────────────────┐
│         Backend FastAPI                  │
│  ┌──────────────────────────────────┐   │
│  │    QueryRouter                   │   │
│  │  - Score les intentions          │   │
│  │  - Décide de la stratégie        │   │
│  └──────────┬───────────────────────┘   │
│             ↓                            │
│  ┌──────────────────────────────────┐   │
│  │   FinancialAgent                 │   │
│  │  - Détecte 145 instruments       │   │
│  │  - Injecte le contexte           │   │
│  └──────────┬───────────────────────┘   │
└─────────────┼───────────────────────────┘
              │
    ┌─────────┼─────────┬─────────────┐
    ↓         ↓         ↓             ↓
┌────────┐ ┌───────┐ ┌─────────┐ ┌──────────┐
│ Ollama │ │  MCP  │ │Knowledge│ │ yfinance │
│Qwen2.5 │ │Server │ │  Base   │ │ Scraping │
│  7B    │ │       │ │         │ │          │
└────────┘ └───────┘ └─────────┘ └──────────┘
```

### Stack technique

| Couche | Technologie | Rôle |
|--------|------------|------|
| **Frontend** | React + Vite + Tailwind | Interface utilisateur |
| **Backend** | Python + FastAPI | Orchestration et API REST |
| **LLM** | Ollama + Qwen2.5:7b | Moteur de raisonnement (32k tokens de contexte) |
| **Router** | Python | Scoring intelligent sur 4 dimensions |
| **Knowledge Base** | JSON | 517 lignes de concepts financiers |
| **MCP** | Python + FastAPI | Serveur de protocole pour outils |
| **Scraping** | yfinance | Données Yahoo Finance temps réel |

## Installation

### Prérequis

Vous aurez besoin de :

- Python 3.10 ou supérieur
- Node.js 18 ou supérieur
- Ollama installé sur votre machine
- Au moins 16 GB de RAM (recommandé : 32 GB)

### Étape 1 : Cloner le projet

```bash
git clone <url-du-repo>
cd "SnT AI"
```

### Étape 2 : Installer et configurer Ollama

Installer Ollama selon votre système :

```bash
# macOS / Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows : Télécharger depuis https://ollama.com/download
```

Vérifier l'installation :

```bash
ollama --version
```

Télécharger le modèle Qwen2.5:7b (environ 4.7 GB) :

```bash
ollama pull qwen2.5:7b
```

Vérifier que le modèle est bien installé :

```bash
ollama list
```

### Étape 3 : Configurer le backend

```bash
cd backend

# Créer un environnement virtuel Python
python3 -m venv venv

# Activer l'environnement
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Installer les dépendances
pip install -r requirements.txt
```

Vérifier que tout fonctionne :

```bash
python -c "import fastapi, ollama, yfinance; print('Dépendances OK')"
```

### Étape 4 : Configurer le frontend

```bash
cd ../frontend

# Installer les dépendances Node
npm install
```

## Démarrage

Le système nécessite trois services qui doivent tourner simultanément. Ouvrez trois terminaux différents :

### Terminal 1 : Serveur MCP (port 8001)

```bash
cd backend
source venv/bin/activate
python -m mcp.mcp_server
```

Vous devriez voir :
```
INFO:     Started server process [xxxxx]
INFO:     Uvicorn running on http://0.0.0.0:8001
```

### Terminal 2 : Backend FastAPI (port 8000)

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

Vous devriez voir :
```
INFO:     Router and Knowledge Base initialized
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Terminal 3 : Frontend React (port 3000)

```bash
cd frontend
npm run dev
```

Vous devriez voir :
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:3000/
```

### Accès à l'application

Une fois les trois services lancés :

- **Application** : http://localhost:3000
- **Documentation API Backend** : http://localhost:8000/docs
- **Documentation MCP** : http://localhost:8001/docs
- **Health check** : http://localhost:8000/health

## Test du système

### Vérifier que tout fonctionne

```bash
# Vérifier le backend
curl http://localhost:8000/health

# Vérifier le MCP Server
curl http://localhost:8001/health

# Vérifier Ollama
ollama list
```

### Tester via l'API

```bash
# Question simple (routage conversationnel)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Bonjour"}'

# Question éducative (routage knowledge base)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Qu'\''est-ce qu'\''un ratio P/E ?"}'

# Question avec données (routage scraping)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Quel est le prix actuel d'\''Apple ?"}'
```

### Observer le routage intelligent

Dans le terminal du backend (Terminal 2), vous verrez des logs détaillés montrant comment le système route chaque requête :

```
============================================================
ROUTING DECISION: KNOWLEDGE
Description: Base de connaissances (concepts financiers)
Scores: {'scraping': 0.0, 'knowledge': 0.4, 'conversational': 0.0, 'hybrid': 0.0}
Ticker detected: None
============================================================
Knowledge Base: 1245 chars injectés
============================================================
RESPONSE GENERATED SUCCESSFULLY
Sources used: knowledge_base
Route: knowledge
Response length: 523 chars
============================================================
```

### Exemples de requêtes par type

| Type de requête | Exemple | Route attendue |
|-----------------|---------|----------------|
| Conversational | "Bonjour, comment vas-tu ?" | conversational |
| Knowledge | "Explique-moi la diversification" | knowledge |
| Scraping | "Prix de LVMH aujourd'hui ?" | scraping |
| Hybrid | "Apple est-elle chère ? Explique le P/E" | hybrid |

## Structure du projet

```
SnT-AI/
├── backend/
│   ├── app/
│   │   ├── main.py              # Application FastAPI
│   │   ├── agent.py             # Agent financier principal
│   │   ├── router.py            # Système de routage intelligent
│   │   ├── knowledge_base.py    # Gestionnaire de la base de connaissances
│   │   ├── config.py            # Configuration
│   │   ├── models.py            # Modèles Pydantic
│   │   └── prompts.py           # Prompts système (1494 lignes)
│   │
│   ├── data/
│   │   ├── knowledge_base.json  # Base de connaissances (517 lignes)
│   │   └── market_data.json     # Cache des données scrapées
│   │
│   ├── mcp/
│   │   ├── mcp_server.py        # Serveur MCP
│   │   └── tools.py             # Outil get_market_data (yfinance)
│   │
│   ├── scraping/
│   │   └── scraping_yfinance.py # Scraper Yahoo Finance
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatBox.jsx      # Interface de chat
│   │   │   └── GlassCard.jsx    # Composant glassmorphism
│   │   ├── services/
│   │   │   └── api.js           # Client API
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

## Fonctionnalités

### Implémentées

**Backend et IA :**

- Backend FastAPI avec endpoints REST
- Agent financier utilisant Ollama et Qwen2.5:7b (32k tokens de contexte)
- System prompt de 1494 lignes avec guardrails éthiques rigoureux
- Routeur intelligent avec scoring sur 4 dimensions
- Base de connaissances structurée (11 concepts + 20 termes + stratégies)
- Détection automatique de 145 instruments (actions, ETF, indices, cryptos)
- Serveur MCP avec outil de scraping yfinance
- Récupération de 25+ métriques financières en temps réel
- Logs détaillés avec traçabilité complète

**Frontend :**

- Interface React moderne avec Vite et Tailwind CSS
- Design glassmorphism avec thème doré
- Chat en temps réel avec gestion du markdown
- Indicateurs de santé des services
- Gestion d'erreurs robuste

**Routage intelligent :**

Le système détermine automatiquement la meilleure stratégie pour chaque requête :

- **SCRAPING** : Données en temps réel (prix, ratios, volume)
- **KNOWLEDGE** : Explications pédagogiques tirées de la base de connaissances
- **CONVERSATIONAL** : Réponses conversationnelles simples
- **HYBRID** : Combinaison de données temps réel et de contenu éducatif

### Points forts techniques

| Aspect | Description |
|--------|-------------|
| **100% Local** | Aucune API externe payante, données privées |
| **Routage précis** | 90% de précision sur les tests |
| **Base de connaissances** | 517 lignes de contenu pédagogique structuré |
| **Couverture large** | 145 instruments financiers supportés |
| **Guardrails éthiques** | Système de protection pour investisseurs débutants |
| **Architecture modulaire** | Séparation claire des responsabilités |

### Améliorations futures

- Gestion de sessions persistantes avec Redis ou SQLite
- Historique des conversations avec possibilité d'export
- Graphiques financiers interactifs
- Mode vocal avec reconnaissance vocale
- Notifications de prix en temps réel
- Suivi de portefeuille et simulations

## Contribution

Ce projet est développé dans le cadre d'un projet académique.

Pour contribuer :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit les changements (`git commit -m 'Ajout de la fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrir une Pull Request

## Dépannage

### Le modèle n'est pas trouvé

Vérifier que Qwen2.5:7b est bien téléchargé :

```bash
ollama list
```

Si absent, le télécharger :

```bash
ollama pull qwen2.5:7b
```

### Port déjà utilisé

Trouver et arrêter le processus qui utilise le port :

```bash
lsof -i :8000  # ou :8001, :3000
kill -9 <PID>
```

### Module Python non trouvé

Vérifier que l'environnement virtuel est activé :

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Réponses lentes

Le modèle Qwen2.5:7b nécessite au moins 8 GB de RAM. Les performances varient selon le matériel :

- Mac M1/M2/M3 : Performances optimales (3-10 secondes)
- CPU Intel/AMD récent : 15-30 secondes par réponse
- GPU NVIDIA : 3-8 secondes avec CUDA

## Crédits

Ce projet utilise les technologies suivantes :

- **Ollama** pour l'exécution locale de modèles de langage
- **Alibaba Cloud** pour le modèle Qwen2.5:7b
- **FastAPI** pour le framework backend
- **React** et **Vite** pour le frontend moderne
- **Tailwind CSS** pour le système de design
- **yfinance** pour l'accès aux données Yahoo Finance
