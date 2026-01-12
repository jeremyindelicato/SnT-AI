# Start&Trade Frontend

Frontend React moderne avec Vite pour l'assistant financier intelligent Start&Trade.

## 🎨 Design

Interface sombre et épurée inspirée du glassmorphism premium :
- **Couleur principale** : Vert émeraude moderne (#10B981)
- **Background** : Noir profond avec effets de blur lumineux
- **Typographie** : Inter (corps) + Space Grotesk (titres)
- **Effets** : Glassmorphism, animations fluides, dégradés subtils

## 📁 Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ChatBox.jsx       # Composant chatbot principal
│   │   └── GlassCard.jsx     # Composant card avec effet glass
│   ├── services/
│   │   └── api.js            # Service de communication avec le backend
│   ├── App.jsx               # Application principale
│   ├── main.jsx              # Point d'entrée React
│   └── index.css             # Styles globaux + Tailwind
├── index.html
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## 🚀 Installation

### Prérequis

- **Node.js 18+** et npm/yarn/pnpm
- **Backend Start&Trade** lancé sur le port 8000

### Installation des dépendances

```bash
cd frontend
npm install
```

### Configuration

Copier le fichier de configuration exemple :

```bash
cp .env.example .env
```

Le fichier `.env` doit contenir :

```env
VITE_API_URL=http://localhost:8000
```

## 🏃 Lancer l'application

### Mode développement (Port 3000)

```bash
npm run dev
```

L'application sera accessible sur **http://localhost:3000**

### Build de production

```bash
npm run build
```

Les fichiers seront générés dans le dossier `dist/`.

### Preview du build

```bash
npm run preview
```

## 🧪 Test de l'application

### 1. Vérifier que le backend est lancé

```bash
curl http://localhost:8000/health
```

Réponse attendue :
```json
{
  "status": "healthy",
  "ollama_connected": true
}
```

### 2. Lancer le frontend

```bash
cd frontend
npm run dev
```

### 3. Ouvrir le navigateur

Naviguer vers **http://localhost:3000**

### 4. Tester le chatbot

Dans l'interface, poser une question comme :
- "Qu'est-ce qu'une action ?"
- "Comment diversifier mon portefeuille ?"
- "Explique-moi les ETF"

## 🎯 Fonctionnalités

### ChatBox Component

- ✅ Interface de chat moderne avec messages utilisateur/assistant
- ✅ Indicateur de statut (backend connecté/déconnecté)
- ✅ Animation de chargement pendant la génération
- ✅ Auto-scroll vers le dernier message
- ✅ Gestion d'erreurs avec messages explicites
- ✅ Bouton de réinitialisation de conversation
- ✅ Vérification de santé du backend

### API Service

- ✅ Communication avec le backend FastAPI
- ✅ Envoi de messages (`/chat`)
- ✅ Health check (`/health`)
- ✅ Réinitialisation (`/chat/reset`)
- ✅ Historique (`/chat/history`)
- ✅ Gestion d'erreurs et timeouts

### Design Components

- ✅ GlassCard : Composant réutilisable avec effet glassmorphism
- ✅ Animations fluides et transitions
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Dark mode par défaut

## 🔧 Configuration Vite

Le fichier [vite.config.js](vite.config.js) configure :
- Port de développement : **3000**
- Proxy API : Redirection de `/api` vers `http://localhost:8000`

## 🎨 Personnalisation

### Changer la couleur principale

Modifier [tailwind.config.js](tailwind.config.js:7-11) :

```js
colors: {
  primary: {
    DEFAULT: '#10B981', // Remplacer par ta couleur
    dark: '#059669',
    light: '#34D399',
  }
}
```

### Modifier le nom de l'assistant

Modifier [ChatBox.jsx](src/components/ChatBox.jsx:74) :

```jsx
<span className="text-xs uppercase tracking-wider font-bold">
  Ton Nom Ici
</span>
```

## 📦 Technologies utilisées

| Technologie | Version | Usage |
|------------|---------|-------|
| React | 18.2 | Framework UI |
| Vite | 5.0 | Build tool ultra-rapide |
| Tailwind CSS | 3.4 | Framework CSS utilitaire |
| Lucide React | 0.309 | Icônes modernes |
| Axios | 1.6 | Client HTTP |

## 🐛 Dépannage

### Le chatbot ne répond pas

1. Vérifier que le backend est lancé :
   ```bash
   curl http://localhost:8000/health
   ```

2. Vérifier qu'Ollama tourne :
   ```bash
   ollama list
   ```

3. Vérifier les logs du navigateur (F12 > Console)

### Erreur CORS

Si tu rencontres des erreurs CORS, vérifie que le backend a bien le middleware CORS activé dans [backend/app/main.py](../backend/app/main.py:51-57).

### Les styles ne s'appliquent pas

1. Vérifier que Tailwind est bien compilé :
   ```bash
   npm run dev
   ```

2. Vider le cache du navigateur (Ctrl+Shift+R)

## 📝 À venir

- [ ] Gestion des sessions persistantes
- [ ] Sauvegarde de l'historique en localStorage
- [ ] Mode clair/sombre toggle
- [ ] Export de conversation en PDF
- [ ] Visualisations de données financières (graphiques)
- [ ] Intégration complète du tool calling MCP

## 🤝 Contribution

Ce projet fait partie du projet HEPHAESTUS. Pour contribuer :

1. Fork le repository
2. Crée une branche (`git checkout -b feature/amazing-feature`)
3. Commit tes changements (`git commit -m 'Add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing-feature`)
5. Ouvre une Pull Request

## 📄 Licence

Projet académique - HEPHAESTUS 2026
