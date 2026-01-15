# 🚀 Start&Trade - Projet HEPHAESTUS

Agent conversationnel intelligent agissant comme conseiller financier pour jeunes investisseurs.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)
![Ollama](https://img.shields.io/badge/ollama-qwen2.5:7b-green.svg)

## 📖 Description

**Start&Trade** est un assistant financier pédagogique propulsé par l'IA, conçu pour accompagner les jeunes investisseurs dans leurs premiers pas sur les marchés financiers. Le projet utilise une architecture moderne et modulaire combinant IA locale, scraping en temps réel, knowledge base pédagogique et système de routage intelligent.

### 🎯 Objectifs

- Fournir un conseiller financier accessible et pédagogique
- Utiliser uniquement des technologies locales et open-source (100% local)
- Récupérer des données financières en temps réel via scraping éthique
- Combiner données temps réel + contenu pédagogique via routage intelligent
- Offrir une expérience utilisateur moderne et fluide

## 🏗️ Architecture

Le projet suit l'architecture **HEPHAESTUS** avec routage intelligent :

```
┌─────────────────┐
│   Frontend      │  React + Vite + Tailwind (Port 3000)
│   (Interface)   │  Glassmorphism design
└────────┬────────┘
         │ HTTP REST
         ↓
┌─────────────────────────────────────────┐
│         Backend FastAPI (Port 8000)      │
│  ┌──────────────────────────────────┐   │
│  │    QueryRouter (Scoring)         │   │
│  │  • Scraping score                │   │
│  │  • Knowledge score               │   │
│  │  • Conversational score          │   │
│  │  • Hybrid score                  │   │
│  └──────────┬───────────────────────┘   │
│             ↓                            │
│  ┌──────────────────────────────────┐   │
│  │   FinancialAgent                 │   │
│  │  • Ticker detection (145 assets) │   │
│  │  • Intelligent routing           │   │
│  │  • Context injection             │   │
│  └──────────┬───────────────────────┘   │
└─────────────┼───────────────────────────┘
              │
    ┌─────────┼─────────┬─────────────┐
    ↓         ↓         ↓             ↓
┌────────┐ ┌───────┐ ┌─────────┐ ┌──────────┐
│ Ollama │ │  MCP  │ │Knowledge│ │ yfinance │
│Qwen2.5 │ │Server │ │  Base   │ │ (Scraper)│
│  7B    │ │ 8001  │ │ (JSON)  │ │          │
└────────┘ └───────┘ └─────────┘ └──────────┘
```

### Stack Technique

| Couche | Technologie | Rôle |
|--------|------------|------|
| **Frontend** | React + Vite + Tailwind | Interface utilisateur moderne avec glassmorphism |
| **Backend** | Python + FastAPI | Orchestrateur et API REST |
| **LLM** | Ollama + Qwen2.5:7b | Moteur de raisonnement IA local (32k context) |
| **Router** | Python (custom) | Système de scoring intelligent (4 dimensions) |
| **Knowledge Base** | JSON (517 lignes) | Concepts financiers + glossaire + stratégies |
| **MCP** | Python | Serveur de protocole pour outils |
| **Scraping** | yfinance | Récupération données Yahoo Finance (25+ metrics) |
| **Assets** | 145 instruments | Actions, ETF, indices, crypto-monnaies |

## 🚀 Installation & Démarrage Complet

### Prérequis

- **Python 3.10+** (vérifier avec `python3 --version`)
- **Node.js 18+** (vérifier avec `node --version`)
- **Ollama** installé localement
- **Git** pour cloner le projet

### 📦 Installation Étape par Étape

#### **Étape 1 : Cloner le projet**

```bash
# Cloner le dépôt
git clone <url-du-repo>
cd "SnT AI"
```

#### **Étape 2 : Installer Ollama**

```bash
# macOS / Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows : Télécharger depuis https://ollama.com/download
```

Vérifier l'installation :
```bash
ollama --version
```

#### **Étape 3 : Télécharger le modèle Qwen2.5:7b**

```bash
# Télécharger le modèle (environ 4.7 GB)
ollama pull qwen2.5:7b

# Vérifier que le modèle est installé
ollama list
```

> **Note** : Le téléchargement prend quelques minutes selon votre connexion.

#### **Étape 4 : Configuration Backend (Python)**

```bash
# Se placer dans le dossier backend
cd backend

# Créer un environnement virtuel
python3 -m venv venv

# Activer l'environnement virtuel
# macOS/Linux :
source venv/bin/activate
# Windows :
# venv\Scripts\activate

# Installer les dépendances Python
pip install -r requirements.txt
```

Vérifier l'installation :
```bash
python -c "import fastapi, ollama, yfinance; print('✅ Dépendances installées')"
```

#### **Étape 5 : Configuration Frontend (React)**

```bash
# Revenir à la racine puis aller dans frontend
cd ..
cd frontend

# Installer les dépendances Node.js
npm install

# Vérifier l'installation
npm list --depth=0
```

### 🚀 Lancement de l'Application

**Important** : Ouvrir **3 terminaux séparés** pour les 3 services.

#### **Terminal 1 : MCP Server** (Port 8001)

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python -m mcp.mcp_server
```

Vous devriez voir :
```
INFO:     Started server process [xxxxx]
INFO:     Uvicorn running on http://0.0.0.0:8001
```

#### **Terminal 2 : Backend FastAPI** (Port 8000)

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

Vous devriez voir :
```
INFO:     Router and Knowledge Base initialized
INFO:     Uvicorn running on http://127.0.0.1:8000
```

#### **Terminal 3 : Frontend React** (Port 3000)

```bash
cd frontend
npm run dev
```

Vous devriez voir :
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
```

### 🌐 Accéder à l'Application

Une fois les 3 services lancés :

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Interface utilisateur principale |
| **Backend API** | http://localhost:8000/docs | Documentation API Swagger |
| **MCP Server** | http://localhost:8001/docs | Documentation MCP Tools |
| **Health Check** | http://localhost:8000/health | Vérification santé backend |

## 🧪 Tests et Vérifications

### Test de Santé des Services

```bash
# 1. Vérifier le backend
curl http://localhost:8000/health
# Réponse attendue : {"status":"healthy","model":"qwen2.5:7b"}

# 2. Vérifier le MCP Server
curl http://localhost:8001/health
# Réponse attendue : {"status":"healthy"}

# 3. Vérifier Ollama
ollama list
# Vous devriez voir qwen2.5:7b dans la liste
```

### Test du Chat (API)

```bash
# Test 1 : Question simple
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Bonjour"}'

# Test 2 : Question éducative (Knowledge Base)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "C'\''est quoi un ratio P/E ?"}'

# Test 3 : Requête de données (Scraping)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Quel est le prix d'\''Apple ?"}'
```

### Observer le Routage Intelligent

Lorsque vous envoyez des messages, regardez les logs du **Terminal 2 (Backend)**. Vous verrez :

```
============================================================
🎯 ROUTING DECISION: KNOWLEDGE
📊 Description: 📚 Base de connaissances (concepts financiers)
📈 Scores: {'scraping': 0.0, 'knowledge': 0.4, 'conversational': 0.0, 'hybrid': 0.0}
🎫 Ticker detected: None
============================================================
✅ Knowledge Base: 1245 chars injectés
============================================================
✅ RESPONSE GENERATED SUCCESSFULLY
📋 Sources used: knowledge_base
🎯 Route: knowledge
💬 Response length: 523 chars
============================================================
```

### Exemples de Requêtes par Type

| Type | Exemple de Question | Route Attendue |
|------|---------------------|----------------|
| **Conversational** | "Bonjour, comment ça va ?" | 💬 conversational |
| **Knowledge** | "Qu'est-ce que la diversification ?" | 📚 knowledge |
| **Scraping** | "Quel est le cours de LVMH ?" | 📊 scraping |
| **Hybrid** | "Apple est-elle chère ? Explique-moi le P/E" | 🔀 hybrid |

## 📁 Structure du Projet

```
SnT-AI/
├── backend/                     # Backend Python FastAPI
│   ├── app/                    # Application principale
│   │   ├── main.py            # FastAPI app & routes
│   │   ├── agent.py           # FinancialAgent (Ollama + Router)
│   │   ├── router.py          # QueryRouter (scoring intelligent) ✨ NEW
│   │   ├── knowledge_base.py  # KnowledgeBase manager ✨ NEW
│   │   ├── config.py          # Configuration
│   │   ├── models.py          # Modèles Pydantic
│   │   └── prompts.py         # System prompts (265 lignes)
│   │
│   ├── data/                   # Données statiques ✨ NEW
│   │   ├── knowledge_base.json # Base de connaissances (517 lignes)
│   │   └── market_data.json    # Cache données scrappées
│   │
│   ├── mcp/                    # Serveur MCP
│   │   ├── mcp_server.py      # Serveur MCP
│   │   └── tools.py           # get_market_data tool (yfinance)
│   │
│   └── requirements.txt        # Dépendances Python
│
├── frontend/                    # Frontend React
│   ├── src/
│   │   ├── components/         # Composants React
│   │   │   ├── ChatBox.jsx    # Chat interface + Markdown processing
│   │   │   └── GlassCard.jsx  # Glassmorphism card
│   │   ├── services/           # Services API
│   │   │   └── api.js
│   │   ├── App.jsx             # Application principale
│   │   ├── index.css           # Styles globaux (gold theme)
│   │   └── main.jsx            # Point d'entrée
│   ├── package.json
│   └── vite.config.js
│
├── project-explaination/        # Documentation du projet
├── test_router_only.py          # Script de test du router ✨ NEW
└── README.md                    # Ce fichier
```

### Fichiers Clés Ajoutés

| Fichier | Lignes | Description |
|---------|--------|-------------|
| `backend/app/router.py` | 185 | Système de scoring sur 4 dimensions |
| `backend/app/knowledge_base.py` | 210 | Gestion de la base de connaissances |
| `backend/data/knowledge_base.json` | 517 | 11 concepts + 20 termes + 10 assets + stratégies |
| `backend/app/agent.py` | 473 | Intégration router + KB (modifié) |

## ✨ Fonctionnalités

### ✅ Implémentées (Version Actuelle)

**Backend & IA :**
- [x] Backend FastAPI avec endpoint `/chat` et `/health`
- [x] Agent FinancialAgent avec Ollama Qwen2.5:7b (32k context)
- [x] System Prompt de 265 lignes avec guardrails éthiques
- [x] **QueryRouter avec scoring intelligent sur 4 dimensions** ⭐
- [x] **Knowledge Base de 517 lignes (11 concepts + 20 termes + stratégies)** ⭐
- [x] Détection de 145 instruments (actions, ETF, indices, crypto)
- [x] Serveur MCP avec tool `get_market_data` (yfinance)
- [x] Scraping Yahoo Finance en temps réel (25+ métriques)
- [x] Logs détaillés avec traçabilité des sources de données

**Frontend :**
- [x] Interface React + Vite + Tailwind CSS
- [x] Design glassmorphism premium avec thème gold
- [x] Chat temps réel avec streaming
- [x] Post-processing Markdown (`**bold**` → HTML)
- [x] Gestion d'erreurs et health checks

**Routage Intelligent :**
- [x] **SCRAPING** : Données temps réel (prix, P/E, volume, etc.)
- [x] **KNOWLEDGE** : Explications pédagogiques (concepts financiers)
- [x] **CONVERSATIONAL** : Réponses LLM pures (salutations, remerciements)
- [x] **HYBRID** : Combinaison données + pédagogie

### 🎯 Points Forts Techniques

| Aspect | Description | Impact |
|--------|-------------|--------|
| **100% Local** | Aucune API externe payante | Gratuit, privé, pas de latence réseau |
| **Routage Intelligent** | 90% de précision (9/10 tests) | Optimisation des réponses selon le contexte |
| **Knowledge Base** | 517 lignes de contenu structuré | Réponses pédagogiques sans scraping |
| **145 Instruments** | Actions FR/US + ETF + Indices + Crypto | Couverture large des marchés |
| **Guardrails Éthiques** | Interdictions, warnings, profil risque | Protection des investisseurs débutants |

### 🚧 Améliorations Futures

- [ ] Gestion de sessions persistantes (Redis/SQLite)
- [ ] Historique de conversations avec export
- [ ] Graphiques financiers interactifs (Chart.js)
- [ ] Mode vocal avec speech-to-text
- [ ] Notifications de prix en temps réel
- [ ] Portfolio tracking et simulations

## 🎨 Captures d'écran

*(À ajouter après première démo)*

## 📚 Documentation

- [Backend README](backend/README.md) - Documentation complète du backend
- [Frontend README](frontend/README.md) - Documentation complète du frontend
- [Project Documentation](project-explaination/project-explaination.md) - Vision et architecture HEPHAESTUS

## 🤝 Contribution

Ce projet est développé dans le cadre du projet académique HEPHAESTUS (8-16 janvier 2026).

Pour contribuer :
1. Fork le projet
2. Créer une branche (`git checkout -b feature/amazing-feature`)
3. Commit les changements (`git commit -m 'Add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

## 📄 Licence

Projet académique - HEPHAESTUS 2026

## 👨‍💻 Auteur

Développé avec ❤️ dans le cadre du projet HEPHAESTUS

## 🔧 Dépannage

### Problème : "Model not found"
```bash
# Vérifier que Qwen2.5 est bien téléchargé
ollama list

# Si absent, télécharger
ollama pull qwen2.5:7b
```

### Problème : "Port already in use"
```bash
# Trouver le processus qui utilise le port
lsof -i :8000  # ou :8001, :3000
kill -9 <PID>  # Remplacer <PID> par le numéro du processus
```

### Problème : "Module 'fastapi' not found"
```bash
# Activer l'environnement virtuel
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate

# Réinstaller les dépendances
pip install -r requirements.txt
```

### Problème : Réponses lentes
- Le modèle Qwen2.5:7b nécessite au moins **8GB de RAM**
- Sur Mac M1/M2/M3/M4 : Performances optimales
- Sur CPU Intel/AMD : ~30-60s par réponse (normal)

## 🙏 Remerciements

- **Ollama** pour l'exécution locale de LLM
- **Alibaba Cloud** pour le modèle Qwen2.5:7b
- **FastAPI** pour le framework backend
- **React** & **Vite** pour le frontend moderne
- **Tailwind CSS** pour le design system
- **yfinance** pour le scraping Yahoo Finance

---

**⚠️ Disclaimer** : Ce projet est un prototype éducatif développé dans le cadre du projet académique HEPHAESTUS. Les informations fournies par l'IA ne constituent pas des conseils financiers professionnels. Tout investissement comporte un risque de perte en capital.
