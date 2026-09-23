# 📁 Structure du Projet Agent Lisa Demo

Guide complet pour comprendre l'organisation du projet.

---

## 🎯 Vue d'ensemble

```
agent-lisa-demo/
├── 🎬 Fichiers de démarrage
├── 📦 src/               → Code source principal
├── 📚 docs/              → Documentation
├── 🧪 scripts/           → Scripts utilitaires
└── ✅ tests/             → Tests unitaires
```

---

## 📄 Fichiers racine

### `main.py`
**Point d'entrée unique du projet**
- Lance l'agent en mode interactif
- Gère les erreurs proprement
- Démarrer avec: `python main.py`

### `README.md`
**Documentation complète du projet**
- Vue d'ensemble
- Guide de démarrage
- Exemples d'utilisation
- Troubleshooting

### `requirements.txt`
**Dépendances Python**
- OpenAI + Azure SDK
- Database (psycopg2)
- Tooling (pytest, black, flake8)
- Installer avec: `pip install -r requirements.txt`

### `setup.ps1`
**Script setup pour Windows**
- Crée automatiquement venv
- Installe dépendances
- Prépare configuration
- Lancer avec: `.\setup.ps1`

### `.env.example`
**Template des variables d'environnement**
- Copier vers `.env` (ne pas committer `.env`!)
- Remplir avec credentials Azure
- Variables:
  - `AZURE_OPENAI_ENDPOINT`
  - `AZURE_OPENAI_API_KEY`
  - `AZURE_OPENAI_DEPLOYMENT_NAME`

### `.gitignore`
**Fichiers à ignorer dans Git**
- `.env` (secrets)
- `venv/` (virtual env)
- `__pycache__/` (cache Python)
- `*.pyc` (bytecode)

### `STRUCTURE.md` (ce fichier)
**Guide d'organisation du projet**

---

## 🔧 `/src` - Code source

### `/src/agent/`
**Cœur du système - Agent Data avec LLM**

#### `__init__.py`
- Expose `DataAgent` et `DataLoader`
- Facilite les imports externes

#### `agent_data.py` ⭐ **PRINCIPAL**
```
Classe: DataAgent
└── __init__()           - Initialise OpenAI + DataLoader
    ├── _load_field_descriptions() - Charge metadonnées LS V3.8.0
    ├── _get_context(query)        - Prépare contexte enrichi
    ├── query(user_query)          - Traite une requête utilisateur
    └── chat()                      - Mode conversation interactif
```

**Responsabilités:**
- Charge données + descriptions
- Envoie contexte au LLM Azure
- Parse réponses + affiche résultats
- Gère mode interactif

#### `data_loader.py` ⭐ **SECONDAIRE**
```
Classe: DataLoader
└── __init__()                   - Charge tous les JSON
    ├── get_dossiers()           - Liste dossiers
    ├── search_dossiers(query)   - Cherche par numéro/client
    ├── get_evenements_by_dossier()  - Événements d'un dossier
    ├── get_dossier_summary()    - Résumé complet (DGEN+DPAY+DGAR)
    └── get_statistics()         - Stats globales
```

**Responsabilités:**
- Charge dossiers.json + enregistrements.json + evenements.json
- Expose méthodes de recherche
- Crée structures de résumé

---

### `/src/data/` 
**Données JSON - Base de données locale**

#### `dossiers.json`
**Table DGEN (Données Générales)**
```json
[
  {
    "id": "DOS001",
    "numero_dossier": "LS-2024-001",
    "client_nom": "Entreprise ABC",
    "statut": "ACTIF",
    "dgen": {
      "montant_principal": 50000.00,
      "type_pret": "CREDIT",
      "taux_interet_base": 4.5,
      ...
    }
  }
]
```

**Contient:** 3 dossiers de démo avec structure DGEN

#### `enregistrements.json`
**Tables DPAY (Payeur) + DGAR (Garanties)**
```json
[
  {
    "id": "ENREG001",
    "dossier_id": "DOS001",
    "type_enregistrement": "PRET",
    "dpay": {
      "numero_payeur": "PAY-2024-001",
      "mode_paiement": "VIR",
      "montant_paiement": 833.33
    },
    "dgar": {
      "type_garantie": "HYPO",
      "montant_garantie": 75000.00,
      ...
    }
  }
]
```

**Contient:** 3 enregistrements avec payeurs + garanties

#### `evenements.json`
**Table EVTDOS (Événements)**
```json
[
  {
    "type_evenement": "DÉBLOCAGE",
    "date_evenement": "2024-01-15",
    "montant_evenement": 50000.00
  }
]
```

**Contient:** 6 événements (DÉBLOCAGE, PAIEMENT, TIRAGE, CLÔTURE)

---

### `/src/config/`
**Configurations et métadonnées**

#### `field_descriptions.json` ⭐ **CRUCIAL**
**Dictionnaire LS V3.8.0 pour contextualiser l'IA**

```json
{
  "dgen": {
    "montant_principal": "Montant normalisé et accordé du dossier",
    "type_pret": "Type: CREDIT / REVOLVING / ...",
    ...
  },
  "dpay": {
    "numero_payeur": "Identifiant unique du payeur",
    "mode_paiement": "VIR / PRLV / CHQ / ...",
    ...
  },
  "dgar": {
    "type_garantie": "HYPO / NANTISSEMENT / PRIVILEGE / ...",
    ...
  },
  "contexte_semantique": {
    "DÉBLOCAGE": "Déblocage initial ou partiel des fonds accordés",
    "REVOLVING": "Crédit revolving avec ligne disponible",
    ...
  }
}
```

**Utilisation:**
- Charge dans `DataAgent.__init__()`
- Intégré au contexte LLM
- Aide l'IA à interpréter codes/abréviations
- Source de vérité pour métadonnées

---

## 📚 `/docs` - Documentation

### `README.md` (à la racine)
- Documentation générale du projet
- Guide démarrage rapide
- Exemple d'utilisation

### `STRUCTURE.md` (ce fichier)
- Guide de chaque dossier/fichier
- Architecture & flux
- Rôles & responsabilités

### `DOSSIER_COMPLETE_SCHEMA.md` ⭐ **REFERENCE**
**Schéma LS V3.8.0 - 25 enregistrements du fichier DOSSIER**
- ENR-DLANC (01) → ENR-DCCBL (23)
- Tous les attributs listés
- Descriptions pour l'IA
- Source: PDF officiel LS V3.8.0

### `LS_V3_8_0_SCHEMA.md`
**Vue d'ensemble des fichiers permanents**
- 20+ fichiers du système LS
- Correspondances entre tables
- Attributs clés pour démo

### `AZURE_VOCABULARY.md`
**Glossaire Azure**
- Tenant, Subscription, Resource Group
- Cognitive Services, Deployment
- Authentification

### `POSTGRES_CONFIG.md`
**Configuration PostgreSQL Flexible Server**
- Paramètres de connexion
- String de connexion
- Résolution de problèmes

---

## 🧪 `/scripts` - Utilitaires & Tests

### `test_demo_ls_v3.py`
**Démo complète des tables avec affichage**
- Affiche statistiques
- Liste tous dossiers + DGEN
- Affiche DPAY + DGAR
- Affiche événements
- Lancer: `python scripts/test_demo_ls_v3.py`

**Sortie:**
```
📊 STATISTIQUES: 180,000€ sur 3 dossiers
📋 DOSSIERS: LS-2024-001, LS-2024-002, LS-2024-003
💳 PAYEURS: PAY-2024-001, PAY-2024-002, PAY-2024-003
🔐 GARANTIES: HYPO, NANTISSEMENT, PRIVILEGE
```

### `test_azure_setup.py`
**Vérifie la connexion Azure**
- Test Azure OpenAI
- Test authentification
- Lancer: `python scripts/test_azure_setup.py`

---

## ✅ `/tests` - Tests unitaires

**À venir (template prêt)**

Structure recommandée:
```
tests/
├── test_data_loader.py
├── test_agent_data.py
└── test_field_descriptions.py
```

Exécuter avec: `pytest tests/`

---

## 🔄 Flux d'exécution

### Démarrage (main.py)
```
main.py
  ↓
DataAgent.__init__()
  ├─ DataLoader() - charge JSON
  ├─ _load_field_descriptions() - charge métadonnées
  └─ Azure OpenAI client init
  ↓
agent.chat() - mode interactif
```

### Requête utilisateur
```
[Utilisateur tape question]
  ↓
DataAgent.query(question)
  ├─ _get_context() - prépare contexte
  │  ├─ Ajoute field_descriptions
  │  ├─ Cherche dossiers pertinents
  │  ├─ Ajoute statistiques
  │  └─ Ajoute événements récents
  ├─ OpenAI LLM (avec contexte)
  └─ Affiche réponse
```

---

## 📦 Dépendances principales

| Paquet | Rôle |
|--------|------|
| `openai` | Azure OpenAI SDK |
| `python-dotenv` | Charge `.env` |
| `psycopg2-binary` | Connexion PostgreSQL (optionnel) |
| `pandas` | Data manipulation (optionnel) |
| `pytest` | Framework tests |

---

## 🚀 Commandes utiles

```bash
# Setup initial
.\setup.ps1

# Lancer l'agent
python main.py

# Voir démo
python scripts/test_demo_ls_v3.py

# Vérifier Azure
python scripts/test_azure_setup.py

# Tests
pytest tests/

# Format code
black src/

# Lint
flake8 src/
```

---

## 💡 Notes importantes

### Ordre de chargement
1. `.env` → Credentials
2. `field_descriptions.json` → Métadonnées
3. `dossiers.json` + `enregistrements.json` + `evenements.json` → Données
4. LLM Azure OpenAI → Intelligence

### Sécurité
- `.env` JAMAIS committer
- `.gitignore` protège secrets
- Credentials dans env variables uniquement

### Extensibilité
- Ajouter tables facile (copier JSON format)
- Ajouter descriptions facile (update field_descriptions.json)
- Ajouter logic facile (étendre DataAgent)

---

**Version:** 1.0.0  
**Date:** 2026-09-23  
**Status:** ✅ Production-ready
