# 🏦 Agent Lisa Demo - LS V3.8.0

**Intelligent LLM Agent for Loan Servicing (LS) V3.8.0 Banking System**

Démonstrateur d'un agent IA capable d'interroger intelligemment une base de données bancaires (dossiers de prêts, enregistrements, événements) en utilisant le schéma réel LS V3.8.0 de Sopra Banking.

---

## 📋 Vue d'ensemble

Cet agent combine :
- ✅ **Azure OpenAI LLM** (gpt-5.4-mini) pour la compréhension naturelle
- ✅ **Schéma LS V3.8.0** avec 25 enregistrements (DGEN, DPAY, DGAR, etc.)
- ✅ **Données JSON locales** pour éviter les contraintes réseau
- ✅ **Dictionnaire de métadonnées** pour contextualiser l'IA
- ✅ **RAG Pattern** : récupération + génération intelligente

### 📊 Tables implémentées

| Table | Description | Attributs clés |
|-------|---|---|
| **DGEN** | Données Générales | montant_principal, devise, type_pret, taux |
| **DPAY** | Données Payeur | numero_payeur, mode_paiement, montant, IBAN |
| **DGAR** | Données Garanties | type_garantie, montant_garanti, % couverture |
| **EVTDOS** | Événements | DÉBLOCAGE, PAIEMENT, TIRAGE, CLÔTURE |

---

## 🚀 Démarrage rapide

### Prérequis
```bash
Python 3.9+
pip / virtualenv
```

### Installation

1. **Cloner & configurer**
```bash
cd agent-lisa-demo
python -m venv venv

# Windows
.\venv\Scripts\Activate

# Linux/Mac
source venv/bin/activate
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configurer les secrets Azure**
```bash
cp .env.example .env

# Éditer .env avec vos credentials:
# - AZURE_OPENAI_ENDPOINT
# - AZURE_OPENAI_API_KEY
# - AZURE_OPENAI_API_VERSION
# - AZURE_OPENAI_DEPLOYMENT_NAME
```

### Utilisation

**Lancer l'agent en mode interactif**
```bash
python -m src.agent.agent_data
```

**Lancer la démo des tables**
```bash
python scripts/test_demo_ls_v3.py
```

---

## 📁 Structure du projet

```
agent-lisa-demo/
├── README.md                          # Ce fichier
├── requirements.txt                   # Dépendances Python
├── .env.example                       # Template variables d'environnement
├── .gitignore                         # Fichiers à ignorer
│
├── src/
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── agent_data.py             # Agent principal avec Azure OpenAI
│   │   └── data_loader.py            # Charge les données JSON
│   │
│   ├── data/
│   │   ├── dossiers.json             # 3 dossiers (DGEN enrichie)
│   │   ├── enregistrements.json       # 3 enregistrements (DPAY + DGAR)
│   │   └── evenements.json            # 6 événements (DÉBLOCAGE, PAIEMENT, etc.)
│   │
│   └── config/
│       └── field_descriptions.json    # Dictionnaire des champs LS V3.8.0
│
├── docs/
│   ├── DOSSIER_COMPLETE_SCHEMA.md     # 25 enregistrements DOSSIER expliqués
│   ├── LS_V3_8_0_SCHEMA.md            # Vue d'ensemble complète
│   ├── AZURE_VOCABULARY.md            # Glossaire Azure
│   └── POSTGRES_CONFIG.md             # Config PostgreSQL Flexible Server
│
├── scripts/
│   ├── test_demo_ls_v3.py             # Affiche les données avec tables
│   └── test_azure_setup.py            # Vérifie la connexion Azure
│
└── tests/
    └── (tests unitaires à venir)
```

---

## 🔄 Flux de fonctionnement

```
[Utilisateur]
      ↓
[Agent Query]
      ↓
[DataLoader] → Charge dossiers.json, enregistrements.json, evenements.json
      ↓
[Field Descriptions] → Ajoute contexte (DGEN, DPAY, DGAR meanings)
      ↓
[_get_context()] → Prépare contexte enrichi pour LLM
      ↓
[Azure OpenAI LLM] → Analyse + génère réponse intelligente
      ↓
[Réponse utilisateur] ✓
```

---

## 💡 Exemples de requêtes

```python
# Créer l'agent
agent = DataAgent()

# Requête 1: Information sur les dossiers
agent.query("Combien de dossiers actifs avons-nous?")
# → "Nous avons 2 dossiers actifs"

# Requête 2: Détails avec tables
agent.query("Quel est le montant total accordé?")
# → "180,000€ répartis sur 3 dossiers"

# Requête 3: Garanties
agent.query("Quelles sont les garanties du dossier DOS001?")
# → "HYPO: 75,000€ (150% de couverture)"

# Requête 4: Événements
agent.query("Quels paiements récents?")
# → Liste événements PAIEMENT avec dates et montants
```

---

## 📊 Données de démo

### Dossiers (Table DGEN)
```json
{
  "dossier": "LS-2024-001",
  "client": "Entreprise ABC",
  "montant": "50,000€",
  "type": "CREDIT",
  "taux": 4.5,
  "statut": "ACTIF"
}
```

### Payeurs (Table DPAY)
```json
{
  "numero_payeur": "PAY-2024-001",
  "mode_paiement": "VIR (virement)",
  "montant_echeance": "833.33€",
  "iban": "FR1420041010050500013M02606"
}
```

### Garanties (Table DGAR)
```json
{
  "type": "HYPO (hypothèque)",
  "montant_garanti": "75,000€",
  "couverture": "150%"
}
```

### Événements
```
DÉBLOCAGE: 50,000€ le 2024-01-15
PAIEMENT: 833.33€ le 2024-02-15
TIRAGE: 25,000€ le 2024-02-20 (revolving)
CLÔTURE: le 2026-09-20
```

---

## 🔐 Sécurité & Configuration

### Variables d'environnement

Voir `.env.example` pour template complet.

**Critiques:**
- `AZURE_OPENAI_ENDPOINT` - URL API Azure OpenAI
- `AZURE_OPENAI_API_KEY` - Clé d'authentification
- `AZURE_OPENAI_DEPLOYMENT_NAME` - Nom déploiement (ex: gpt-5.4-mini)

### Fichiers ignorés

`.gitignore` exclut automatiquement:
- `.env` (credentials)
- `__pycache__/` (cache Python)
- `venv/` (virtual environment)
- `*.pyc` (fichiers compilés)

---

## 📈 Points forts de cette implémentation

✅ **Schéma réaliste** : 25 enregistrements du vrai LS V3.8.0  
✅ **Contextualisation IA** : Dictionnaire de 50+ descriptions de champs  
✅ **Pas de DB réseau** : JSON local = pas de timeout (tested! 🎯)  
✅ **Prêt pour production** : Structure professionnelle & modulaire  
✅ **Extensible** : Facile d'ajouter LIGNE, REVOLVING, EVTIMP, etc.  
✅ **Documenté** : 4 fichiers de docs (schémas, Azure, Postgres)  

---

## 🔮 Évolutions possibles

- [ ] Ajouter tables LIGNE (enregistrements) + REVOLVING
- [ ] Implémenter ECHIMP (échéances impayées) pour scénarios dégradés
- [ ] Connecter PostgreSQL Flexible Server Azure (réseau stable)
- [ ] API REST FastAPI pour exposer l'agent
- [ ] Dashboard web pour visualiser dossiers + garanties
- [ ] Tests unitaires complets
- [ ] CI/CD avec GitHub Actions

---

## 📞 Support

Pour questions sur l'implémentation :
- Voir `docs/` pour documentation détaillée
- Consulter `DOSSIER_COMPLETE_SCHEMA.md` pour mapping complet LS V3.8.0
- Voir `src/config/field_descriptions.json` pour sens des codes

---

## 📄 Licence

Hackathon RBS 2026  
Copyright © 2026

---

**Dernière mise à jour** : 2026-09-23  
**Version** : 1.0.0 (Démo)  
**Statut** : ✅ Prêt pour présentation
