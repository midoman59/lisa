# 🏗️ Architecture de l'Agent LISA

**Comprendre comment fonctionne le système d'un coup d'œil.**

---

## 📊 Flux Global

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                       │
│  [Utilisateur]  →  [Agent LISA]  →  [DataLoader]  →  [JSON Local]  │
│      ↓                                                       ↓       │
│    Question                                           Dossiers      │
│  "Combien de       ┌──────────────────────────────────────┘        │
│   dossiers?"       │                                                │
│      ↓             ↓                                                │
│     Agent         Agent cherche contexte                            │
│   reçoit la      + prépare les données                             │
│   question           ↓                                              │
│                  [Azure OpenAI] ☁️                                 │
│                   (Réfléchit)                                       │
│                      ↓                                              │
│                 [Réponse IA]                                       │
│                      ↓                                              │
│                  Affichage                                          │
│           "Vous avez 2 dossiers actifs"                            │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Les 6 Étapes du Processus

### **1️⃣ Utilisateur pose une question**
```
[Vous] > Combien de dossiers actifs avons-nous?
```
Le message arrive à l'agent.

---

### **2️⃣ Agent cherche dans les données locales**
L'`agent_data.py` reçoit la question et demande au `DataLoader` de chercher les données pertinentes.

**Code:**
```python
agent = DataAgent()
agent.query("Combien de dossiers actifs avons-nous?")
```

---

### **3️⃣ DataLoader lit les fichiers JSON**
`DataLoader` va chercher dans `src/data/` :
- **dossiers.json** → 3 dossiers (2 ACTIF, 1 FERMÉ)
- **enregistrements.json** → enregistrements (DGEN, DPAY, DGAR)
- **événements.json** → 6 événements

**Code:**
```python
loader = DataLoader()
dossiers = loader.get_dossiers()          # → 3 dossiers
actifs = loader.get_dossiers_by_statut("ACTIF")  # → 2 dossiers
```

---

### **4️⃣ Agent prépare le contexte**
L'agent prépare un **contexte riche** avec :
- Les statistiques (total, actifs, montant total)
- Les dossiers trouvés avec tous leurs détails (DGEN, DPAY, DGAR)
- Les événements récents
- Le dictionnaire LS V3.8.0 (descriptions des champs)

**Ce contexte est envoyé à Azure avec la question.**

---

### **5️⃣ Azure OpenAI répond**
Azure reçoit :
```
CONTEXTE:
- Total dossiers: 3
- Dossiers actifs: 2
- Montant total: 180 000 €
- Dossiers: [DOS001, DOS002, DOS003]
  - DGEN (données générales): montant_principal, type_pret, etc.
  - DPAY (données payeurs): ...
  - DGAR (données garanties): ...
- Événements récents: [EVT001, EVT002, ...]

QUESTION: Combien de dossiers actifs avons-nous?
```

Le modèle **gpt-5.4-mini** comprend le contexte métier et génère une réponse intelligente.

---

### **6️⃣ Réponse affichée à l'utilisateur**
```
[AGENT] Nous avons **2 dossiers actifs**.
```

La réponse est :
- ✅ Basée sur les données réelles
- ✅ Générée par l'IA
- ✅ En français
- ✅ Intelligente (comprend le contexte LS V3.8.0)

---

## 🧩 Composants Détaillés

### **DataAgent** (`src/agent/agent_data.py`)
**Rôle:** Chef d'orchestre - coordonne tout

**Responsabilités:**
- Reçoit les questions de l'utilisateur
- Initialise le DataLoader
- Prépare le contexte pour Azure
- Appelle Azure OpenAI
- Retourne la réponse
- Gère le mode conversation interactif

**Pseudocode:**
```python
class DataAgent:
    def __init__(self):
        self.loader = DataLoader()          # Charge les données
        self.client = AzureOpenAI(...)      # Connexion Azure
    
    def query(self, user_question):
        context = self._get_context(user_question)  # Prépare contexte
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Tu es un expert en Lisa"},
                {"role": "system", "content": context},  # ← Contexte riche
                {"role": "user", "content": user_question}
            ]
        )
        return response.choices[0].message.content
```

---

### **DataLoader** (`src/agent/data_loader.py`)
**Rôle:** Accès aux données - lit et gère les JSON

**Responsabilités:**
- Charge les fichiers JSON depuis `src/data/`
- Fournit des méthodes pour chercher les données:
  - `get_dossiers()` → tous les dossiers
  - `get_dossiers_by_statut(statut)` → dossiers par statut
  - `search_dossiers(query)` → cherche par numéro ou client
  - `get_evenements_recents(limit)` → événements récents
  - `get_dossier_summary(id)` → résumé complet avec DGEN+DPAY+DGAR
  - `get_statistics()` → statistiques globales

**Pseudocode:**
```python
class DataLoader:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
        self.dossiers = self._load_json("dossiers.json")
        self.enregistrements = self._load_json("enregistrements.json")
        self.evenements = self._load_json("evenements.json")
    
    def get_dossiers_by_statut(self, statut):
        return [d for d in self.dossiers if d.get("statut") == statut]
```

---

### **Données JSON** (`src/data/`)
**Rôle:** Stockage des données pour développement MVP

**Fichiers:**
- `dossiers.json` → 3 dossiers avec structure LS V3.8.0
- `enregistrements.json` → 3 enregistrements (DGEN, DPAY, DGAR)
- `événements.json` → 6 événements

**Structure LS V3.8.0:**
```json
{
  "id": "DOS001",
  "numero_dossier": "LS-2024-001",
  "statut": "ACTIF",
  "dgen": {
    "montant_principal": 100000,
    "type_pret": "REVOLVING",
    "date_octroi": "2024-01-10",
    "couverture_garantie": 85000
  },
  "dpay": [{ "nom_payeur": "...", "iban": "..." }],
  "dgar": [{ "type_garantie": "HYPOTHEQUE", "montant": "..." }]
}
```

---

### **Azure OpenAI** (☁️ Cloud)
**Rôle:** Intelligence artificielle - génère les réponses

**Configuration:**
- **Endpoint:** `https://lisa-creditme.services.ai.azure.com/`
- **Modèle:** `gpt-5.4-mini`
- **API Version:** `2025-04-01-preview`

**Ce qu'il fait:**
1. Reçoit le contexte (données LS V3.8.0)
2. Reçoit la question utilisateur
3. Comprend le domaine métier (crédit, dossiers, garanties)
4. Génère une réponse intelligente et précise

**Avantages:**
- ✅ Comprend le français
- ✅ Comprend le contexte métier (passé dans le prompt)
- ✅ Génère des réponses naturelles
- ✅ Scalable et fiable

---

## 🏢 Structure du Projet

```
agent-lisa-demo/
├── main.py                         ← Point d'entrée
├── .env                            ← Credentials Azure (secret!)
├── src/
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── agent_data.py           ← DataAgent (chef d'orchestre)
│   │   └── data_loader.py          ← DataLoader (accès données)
│   ├── data/
│   │   ├── dossiers.json           ← 3 dossiers
│   │   ├── enregistrements.json    ← 3 enregistrements (DGEN, DPAY, DGAR)
│   │   └── événements.json         ← 6 événements
│   └── config/
│       └── field_descriptions.json ← Dictionnaire LS V3.8.0
├── docs/                           ← Documentation LS V3.8.0
├── scripts/
│   ├── test_azure_setup.py        ← Test connexion Azure
│   └── test_demo_ls_v3.py         ← Voir les données
├── README.md                       ← Vue générale
├── GETTING_STARTED.md             ← Pour débuter rapidement
├── PYTHON_BASICS.md               ← Pour devs zéro Python
├── JUNIOR_GUIDE.md                ← Architecture détaillée
└── ARCHITECTURE.md                ← Ce fichier!
```

---

## 🔄 Flux de Données Complet

### Étape 1: Utilisateur → Agent
```
[INPUT] "Combien de dossiers actifs?"
         ↓
    DataAgent.query()
```

### Étape 2: Agent → DataLoader
```
     DataAgent
         ↓
    DataLoader.get_dossiers()
    DataLoader.get_dossiers_by_statut("ACTIF")
    DataLoader.get_statistics()
    DataLoader.get_evenements_recents()
         ↓
    [DONNÉES CHARGÉES]
```

### Étape 3: Préparer Contexte
```
    DataAgent._get_context()
         ↓
    Prépare string massive:
    - Dictionnaire des champs DGEN, DPAY, DGAR
    - Statistiques
    - Dossiers trouvés avec structure complète
    - Événements récents
         ↓
    [CONTEXTE RICHE]
```

### Étape 4: Agent → Azure
```
    AzureOpenAI.chat.completions.create(
        messages=[
            {"role": "system", "content": "Tu es un expert..."},
            {"role": "system", "content": CONTEXTE_RICHE},  ← Clé!
            {"role": "user", "content": user_question}
        ]
    )
         ↓
    [ENVOI À AZURE]
```

### Étape 5: Azure → Réponse
```
    Azure OpenAI (gpt-5.4-mini)
         ↓
    Analyse question + contexte
    Génère réponse intelligente
         ↓
    "Nous avons 2 dossiers actifs."
```

### Étape 6: Réponse → Utilisateur
```
    [AFFICHAGE]
    [AGENT] Nous avons **2 dossiers actifs**.
         ↓
    Utilisateur voit la réponse
```

---

## 🔐 Sécurité & Secrets

### `.env` (JAMAIS committer!)
```bash
AZURE_OPENAI_ENDPOINT=https://...      # URL Azure
AZURE_OPENAI_API_KEY=A2zB997...        # Clé secrète
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-5.4-mini
```

### `.gitignore` (protection)
```bash
.env        # Empêche de committer les secrets
*.env       # Protège tous les fichiers .env
```

**Chargement sécurisé:**
```python
from dotenv import load_dotenv
import os

load_dotenv()  # Charge depuis .env
api_key = os.getenv("AZURE_OPENAI_API_KEY")  # Récupère la clé
```

---

## 📈 Évolution Future

### Phase MVP (Actuelle)
- ✅ Données JSON locales
- ✅ Agent simple avec Azure OpenAI
- ✅ Mode conversation interactif

### Phase 1 (Prochaine)
- 🔜 Connexion PostgreSQL réelle
- 🔜 Rapatrier les vrais enregistrements DGEN, DPAY, DGAR
- 🔜 Ajouter l'indexation Azure Search (RAG)

### Phase 2 (Plus tard)
- 🔜 Dashboard web
- 🔜 Intégration avec système Lisa existant
- 🔜 Authentification utilisateurs
- 🔜 Audit & logging avancé

---

## 🚀 Pour Tester l'Architecture

### Test 1: Voir les données
```bash
python scripts/test_demo_ls_v3.py
```
Affiche les 3 dossiers, leurs structures DGEN/DPAY/DGAR, et les événements.

### Test 2: Tester Azure
```bash
python scripts/test_azure_setup.py
```
Vérifie que la connexion Azure fonctionne.

### Test 3: Lancer l'agent
```bash
python main.py
```
Pose des questions:
```
[Vous] > Combien de dossiers actifs?
[AGENT] Nous avons 2 dossiers actifs.

[Vous] > Quel est le montant total accordé?
[AGENT] Le montant total accordé est de 180 000 €.

[Vous] > Quels sont les événements récents?
[AGENT] Voici les 6 événements...
```

---

## 📚 Vocabulaire LS V3.8.0

| Terme | Signification |
|-------|---------------|
| **DGEN** | **Données Générales** - Infos principales du dossier (montant, type prêt, etc.) |
| **DPAY** | **Données Payeur** - Infos du client (nom, IBAN, adresse) |
| **DGAR** | **Données Garanties** - Infos sur les garanties (hypothèque, nantissement) |
| **EVTDOS** | **Événement Dossier** - Événement au niveau du dossier |
| **DOSSIER** | Représente un prêt/crédit |
| **ENREGISTREMENT** | Contient DGEN + DPAY + DGAR pour un dossier |
| **ÉVÉNEMENT** | Action (paiement, tirage, clôture, etc.) |

---

## ❓ Questions Fréquentes

**Q: Pourquoi JSON et pas PostgreSQL?**  
A: MVP rapide sans connexion DB. Phase 1 intègrera PostgreSQL réelle.

**Q: Pourquoi Azure et pas autre LLM?**  
A: Parce que c'est ce qu'a la boîte (lisa-creditme resource).

**Q: Comment ça marche offline?**  
A: Les données JSON sont locales, mais Azure nécessite Internet.

**Q: Comment ajouter une question personnalisée?**  
A: Modifie `main.py` et ajoute dans `test_queries`.

**Q: Comment modifier les données de test?**  
A: Édite les fichiers JSON dans `src/data/`.

---

## 🎓 Pour Aller Plus Loin

- Lire [JUNIOR_GUIDE.md](JUNIOR_GUIDE.md) pour architecture détaillée
- Lire [PYTHON_BASICS.md](PYTHON_BASICS.md) si zéro Python
- Explorer `src/agent/agent_data.py` (le cœur du système)
- Consulter `docs/` pour la documentation LS V3.8.0 complète

---

**Version:** 1.0  
**Date:** 2026-09-24  
**Pour:** Comprendre l'architecture complète du système Agent LISA
