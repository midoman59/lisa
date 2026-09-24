# 🎓 Guide pour Développeurs Junior
**Agent Lisa Demo - LS V3.8.0**

*Si tu viens de Java/Angular, ce guide t'explique tout en termes que tu connais ! 👨‍💻*

---

## 🎯 Avant de commencer - 5 minutes pour comprendre

### "C'est quoi ce projet ?"

```
C'est une APPLICATION PYTHON qui:
✓ Pose des questions sur des prêts bancaires
✓ Une IA (Azure OpenAI) répond intelligemment
✓ Les données viennent de fichiers JSON locaux
✓ C'est comme un chatbot pour système bancaire
```

### "Quelle est l'architecture ?"

```
┌─────────────────┐
│   Utilisateur   │  ← Toi, posant une question
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│   main.py               │  ← Point d'entrée (comme Main.java)
│   (lance l'app)         │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│   DataAgent             │  ← Classe principale
│   (gère la logique)     │
└────────┬────────────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐  ┌─────────────┐
│ Azure  │  │ DataLoader  │  ← Charge les données JSON
│ OpenAI │  │ (gère BDD)  │
└────────┘  └──────┬──────┘
                   │
            ┌──────┴──────┬──────────┬──────────┐
            ▼             ▼          ▼          ▼
         DGEN          DPAY       DGAR      EVTDOS
      (dossiers)    (payeurs)  (garanties) (événements)
```

---

## 📦 Structure du projet (comme Maven/Angular)

### En Java/Maven, tu as:
```
projet-maven/
├── pom.xml (dépendances)
├── src/main/java/
│   ├── com/example/agent/
│   │   ├── DataAgent.java
│   │   └── DataLoader.java
│   └── Main.java
└── README.md
```

### En Python (agent-lisa-demo), c'est:
```
agent-lisa-demo/
├── requirements.txt        ← Comme pom.xml (dépendances)
├── main.py                 ← Comme Main.java (point d'entrée)
├── src/
│   ├── agent/             ← Package (dossier avec __init__.py)
│   │   ├── __init__.py    ← Déclare le package (comme package.java)
│   │   ├── agent_data.py  ← Classe DataAgent
│   │   └── data_loader.py ← Classe DataLoader
│   ├── data/              ← Données JSON
│   │   ├── dossiers.json
│   │   ├── enregistrements.json
│   │   └── evenements.json
│   └── config/            ← Configuration
│       └── field_descriptions.json
├── docs/                  ← Documentation
├── scripts/               ← Tests & démos
└── README.md
```

---

## 🚀 Démarrage (5 étapes)

### 1️⃣ Cloner le repo
```bash
git clone https://github.com/midoman59/lisa.git
cd lisa
```

### 2️⃣ Installer l'environnement
```bash
# Windows (PowerShell)
.\setup.ps1

# Linux/Mac (Bash)
./setup.sh  # (à créer)
```

**Qu'est-ce qui se passe ?**
- Crée un `venv` (virtual environment) = comme un conteneur Docker pour les dépendances
- Installe les packages Python de `requirements.txt`
- Configure `.env` (variables d'environnement)

### 3️⃣ Configurer les credentials Azure
Édite le fichier `.env` :
```
AZURE_OPENAI_ENDPOINT=https://...
AZURE_OPENAI_API_KEY=sk-...
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-5.4-mini
```

(Demande les credentials à un senior)

### 4️⃣ Lancer l'app
```bash
python main.py
```

### 5️⃣ Poser une question ! 🎉
```
[Vous] > Combien de dossiers actifs avons-nous?

[AGENT] Nous avons 2 dossiers actifs
```

---

## 🏗️ Architecture expliquée simplement

### Les 3 couches

```
┌─────────────────────────────────────┐
│   COUCHE PRÉSENTATION               │
│   main.py → DataAgent.chat()        │  ← Interface utilisateur
└─────────────────────────────────────┘
                 ▲
                 │
┌─────────────────────────────────────┐
│   COUCHE MÉTIER                     │
│   DataAgent class                   │  ← Logique de l'app
│   • query() → traite la question    │  ← Appelle Azure OpenAI
│   • _get_context() → prépare données│
└─────────────────────────────────────┘
                 ▲
                 │
┌─────────────────────────────────────┐
│   COUCHE DONNÉES                    │
│   DataLoader class                  │  ← Accès aux données
│   • load_all() → charge JSON        │
│   • search_dossiers()               │
└─────────────────────────────────────┘
```

### Fichiers clés

| Fichier | Rôle | Équivalent Java |
|---------|------|-----------------|
| `main.py` | Lance l'app | `Main.java` |
| `src/agent/agent_data.py` | Logique principale | `Service.java` |
| `src/agent/data_loader.py` | Gère la BDD | `Repository.java` |
| `src/data/*.json` | Données | Base de données |
| `.env` | Configuration | `application.properties` |
| `requirements.txt` | Dépendances | `pom.xml` |

---

## 💻 Les classes principales

### `DataAgent` (src/agent/agent_data.py)

**C'est quoi ?** La classe principale qui gère tout

```python
class DataAgent:
    
    def __init__(self):
        # Constructeur (comme en Java)
        self.loader = DataLoader()  # Crée un DataLoader
        self.client = AzureOpenAI(...)  # Se connecte à Azure
    
    def query(self, user_query: str) -> str:
        # Traite une question
        context = self._get_context(user_query)  # Récupère les données
        response = self.client.chat.completions.create(...)  # Appelle OpenAI
        return response  # Retourne la réponse
    
    def chat(self):
        # Mode conversation interactif
        while True:
            question = input("[Vous] > ")
            self.query(question)
```

**Parallèle Java :**
```java
public class DataAgent {
    private DataLoader loader;
    private OpenAIClient client;
    
    public DataAgent() {
        this.loader = new DataLoader();
        this.client = new OpenAIClient(...);
    }
    
    public String query(String userQuery) {
        String context = getContext(userQuery);
        String response = client.chat(context);
        return response;
    }
}
```

### `DataLoader` (src/agent/data_loader.py)

**C'est quoi ?** Charge et expose les données

```python
class DataLoader:
    
    def __init__(self):
        # Charge les fichiers JSON au démarrage
        self.dossiers = self._load_json("dossiers.json")
        self.enregistrements = self._load_json("enregistrements.json")
        self.evenements = self._load_json("evenements.json")
    
    def search_dossiers(self, query: str):
        # Cherche un dossier par numéro ou client
        return [d for d in self.dossiers if query in d["numero_dossier"]]
    
    def get_dossier_summary(self, dossier_id: str):
        # Retourne un résumé complet du dossier
        return {...}
```

**Parallèle Java :**
```java
public class DataLoader {
    private List<Dossier> dossiers;
    private List<Enregistrement> enregistrements;
    
    public DataLoader() {
        this.dossiers = loadJson("dossiers.json");
        // ...
    }
    
    public List<Dossier> searchDossiers(String query) {
        return dossiers.stream()
            .filter(d -> d.getNumeroDossier().contains(query))
            .collect(Collectors.toList());
    }
}
```

---

## 📊 Les données (tables LS V3.8.0)

### Table DGEN (Données Générales)

```json
{
  "id": "DOS001",
  "numero_dossier": "LS-2024-001",
  "dgen": {
    "montant_principal": 50000.00,
    "type_pret": "CREDIT",
    "taux_interet_base": 4.5,
    "duree_mois": 60
  }
}
```

**C'est quoi ?** Les infos de base d'un prêt (montant, taux, durée, etc.)

### Table DPAY (Payeur)

```json
{
  "numero_payeur": "PAY-2024-001",
  "mode_paiement": "VIR",
  "montant_paiement": 833.33,
  "reference_compte": "FR14..."
}
```

**C'est quoi ?** Info du client qui paye (compte, mode de paiement)

### Table DGAR (Garanties)

```json
{
  "type_garantie": "HYPO",
  "montant_garanti": 75000.00,
  "pourcentage_couverture": 150.0
}
```

**C'est quoi ?** Ce qui garantit le prêt (hypothèque, nantissement)

---

## 🔄 Flux d'une requête (étape par étape)

### Quand tu tapes: `"Quel est le montant total ?"`

```
1. Utilisateur tape la question
   └─> main.py lance agent.query()

2. DataAgent.query() reçoit la question
   └─> Appelle _get_context()

3. _get_context() récupère les données
   └─> DataLoader.search_dossiers("montant")
   └─> Retourne dossiers pertinents + statistiques

4. Contexte enrichi envoyé à Azure OpenAI
   └─> "Voici les données: [JSON]"
   └─> "Question de l'utilisateur: [Question]"

5. Azure OpenAI analyse et répond
   └─> "Le montant total est 180,000€"

6. Réponse affichée à l'utilisateur
   └─> "[AGENT] Le montant total est 180,000€"
```

---

## 🐛 Déboguer - Commandes utiles

### Voir les données chargées
```bash
python scripts/test_demo_ls_v3.py
```

### Vérifier la connexion Azure
```bash
python scripts/test_azure_setup.py
```

### Voir l'état du code
```bash
git status
git log --oneline
```

### Voir les variables chargées
```python
# Dans main.py ou un test
from src.agent import DataAgent
agent = DataAgent()
print(agent.loader.dossiers)  # Affiche tous les dossiers
```

---

## ✅ Checklist - Avant de committer du code

- [ ] Le code fonctionne (`python main.py` OK)
- [ ] Les tests passent (`pytest tests/`)
- [ ] Pas de credentials en dur (tout dans `.env`)
- [ ] Docstrings ajoutées ("""...""")
- [ ] `.gitignore` ignorerait mon .env
- [ ] Message de commit clair

---

## 📚 Ressources pour apprendre

### Python basics (15 min)
- Indentation (pas de `{}` !)
- Listes vs dictionnaires
- Classes et `__init__`
- Imports avec `from ... import`

### Git basics (10 min)
```bash
git status
git add .
git commit -m "description"
git push
```

### JSON (5 min)
```json
{
  "key": "value",
  "array": [1, 2, 3],
  "nested": {"inner": "object"}
}
```

---

## ❓ Questions fréquentes

**Q: Pourquoi `.gitignore` ignore `.env` ?**
A: Pour ne pas partager les credentials (clés Azure, mots de passe)

**Q: C'est quoi `__init__.py` ?**
A: Fichier qui dit "ce dossier est un package Python" (comme `package.json` pour Node)

**Q: Comment ajouter une nouvelle table de données ?**
A: 
1. Ajouter `ma_table.json` dans `src/data/`
2. Charger dans `DataLoader.__init__()`
3. Ajouter une méthode `get_ma_table()`

**Q: Je dois modifier le LLM ?**
A: Oui ! Dans `DataAgent._get_context()` tu contrôles quelles données envoyer à Azure

**Q: Comment tester mon code ?**
A: Crée un fichier dans `scripts/test_*.py`, puis `python scripts/test_monfichier.py`

---

## 🎯 Prochaines étapes

1. ✅ Cloner et lancer l'app (`python main.py`)
2. ✅ Poser quelques questions
3. ✅ Lire `src/agent/agent_data.py` (15 min)
4. ✅ Lire `src/agent/data_loader.py` (10 min)
5. ✅ Modifier une question / ajouter une requête test
6. ✅ Créer une branche et commit

---

## 📞 Besoin d'aide ?

- Pas de credentials ? → Demande à un senior
- Code qui fonctionne pas ? → Regarde `git status` et `.env`
- Pas de package Python ? → `pip install -r requirements.txt`
- Azure ne répond pas ? → Vérifier les credentials dans `.env`

**Bienvenue dans l'équipe ! 🚀**

---

**Version**: 1.0  
**Date**: 2026-09-24  
**Pour**: Développeurs juniors
