# 🚀 Start&Trade - Projet HEPHAESTUS

Agent conversationnel intelligent agissant comme conseiller financier pour jeunes investisseurs.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)

## 📖 Description

**Start&Trade** est un assistant financier pédagogique propulsé par l'IA, conçu pour accompagner les jeunes investisseurs dans leurs premiers pas sur les marchés financiers. Le projet utilise une architecture moderne et modulaire combinant IA locale, scraping en temps réel et interface web intuitive.

### 🎯 Objectifs

- Fournir un conseiller financier accessible et pédagogique
- Utiliser uniquement des technologies locales et open-source
- Récupérer des données financières en temps réel de manière éthique
- Offrir une expérience utilisateur moderne et fluide

## 🏗️ Architecture

Le projet suit l'architecture **HEPHAESTUS** :

```
┌─────────────────┐
│   Frontend      │  React + Vite (Port 3000)
│   (Interface)   │
└────────┬────────┘
         │ HTTP
         ↓
┌─────────────────┐
│   Backend       │  FastAPI (Port 8000)
│  (Orchestrator) │
└────────┬────────┘
         │
    ┌────┴─────┬──────────┐
    │          │          │
    ↓          ↓          ↓
┌────────┐ ┌───────┐ ┌──────┐
│ Ollama │ │  MCP  │ │ n8n  │
│ Phi3.5 │ │Server │ │Scraper│
└────────┘ └───────┘ └──────┘
```

### Stack Technique

| Couche | Technologie | Rôle |
|--------|------------|------|
| **Frontend** | React + Vite + Tailwind | Interface utilisateur moderne |
| **Backend** | Python + FastAPI | Orchestrateur et API REST |
| **LLM** | Ollama + Phi 3.5 Mini | Moteur de raisonnement IA local |
| **MCP** | Python | Serveur de protocole pour outils |
| **Scraping** | n8n (à venir) | Récupération données Yahoo Finance |

## 🚀 Installation & Démarrage

### Prérequis

- **Python 3.10+**
- **Node.js 18+**
- **Ollama** avec le modèle Phi 3.5

### 1. Installer Ollama et le modèle

```bash
# Installer Ollama depuis https://ollama.ai
# Puis télécharger le modèle Phi 3.5
ollama pull phi3.5
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

### 4. Lancer l'application

**Terminal 1 - Backend** (Port 8000) :
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend** (Port 3000) :
```bash
cd frontend
npm run dev
```

**Terminal 3 - MCP Server** (Port 8001, optionnel) :
```bash
cd backend
python -m mcp.mcp_server
```

### 5. Accéder à l'application

- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:8000/docs
- **MCP Server** : http://localhost:8001/docs

## 🧪 Test Rapide

```bash
# Vérifier le backend
curl http://localhost:8000/health

# Tester le chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Qu'\''est-ce qu'\''une action ?"}'
```

## 📁 Structure du Projet

```
SnT-AI/
├── backend/                  # Backend Python FastAPI
│   ├── app/                 # Application principale
│   │   ├── main.py         # FastAPI app & routes
│   │   ├── agent.py        # FinancialAgent (Ollama)
│   │   ├── config.py       # Configuration
│   │   ├── models.py       # Modèles Pydantic
│   │   └── prompts.py      # System prompts
│   ├── mcp/                # Serveur MCP
│   │   ├── mcp_server.py  # Serveur MCP
│   │   └── tools.py       # Définition des outils
│   └── requirements.txt    # Dépendances Python
│
├── frontend/                # Frontend React
│   ├── src/
│   │   ├── components/     # Composants React
│   │   │   ├── ChatBox.jsx
│   │   │   └── GlassCard.jsx
│   │   ├── services/       # Services API
│   │   │   └── api.js
│   │   ├── App.jsx         # Application principale
│   │   └── main.jsx        # Point d'entrée
│   ├── package.json
│   └── vite.config.js
│
├── project-explaination/    # Documentation du projet
└── README.md               # Ce fichier
```

## ✨ Fonctionnalités

### ✅ Implémentées

- [x] Backend FastAPI avec endpoint `/chat`
- [x] Agent FinancialAgent communiquant avec Ollama
- [x] System Prompt personnalisé Start&Trade Assistant
- [x] Serveur MCP avec outil `get_market_data` (squelette)
- [x] Frontend React moderne avec Tailwind CSS
- [x] Interface de chat temps réel
- [x] Design glassmorphism premium
- [x] Gestion d'erreurs et health checks

### 🚧 En cours / À venir

- [ ] Intégration n8n pour scraping Yahoo Finance
- [ ] Tool calling complet (MCP ↔ Agent)
- [ ] Gestion de sessions persistantes
- [ ] Historique de conversations
- [ ] Graphiques financiers interactifs
- [ ] Export de conversations en PDF

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

## 🙏 Remerciements

- **Ollama** pour l'exécution locale de LLM
- **Microsoft** pour le modèle Phi 3.5
- **FastAPI** pour le framework backend
- **React** & **Vite** pour le frontend moderne
- **Tailwind CSS** pour le design system

---

**Note** : Ce projet est un prototype éducatif. Les conseils financiers fournis par l'IA ne constituent pas des recommandations d'investissement professionnelles.
