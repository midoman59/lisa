# 🚀 Getting Started - Ultra Simple

**Pour quelqu'un qui vient de cloner le repo et veut juste que ça marche.**

---

## 📋 Prérequis (5 min de setup)

### ✅ Vérifier que Python est installé
```bash
python --version
```

**Doit afficher:** `Python 3.9` ou plus récent

**Si erreur:** Télécharge Python depuis https://www.python.org (Windows) ou utilise `brew install python3` (Mac)

### ✅ Vérifier que Git est installé
```bash
git --version
```

**Doit afficher:** `git version 2.x.x`

---

## 🎯 Étape 1 : Cloner le repo (2 minutes)

```bash
git clone https://github.com/midoman59/lisa.git
cd lisa
```

**Résultat:** Tu es maintenant dans le dossier `lisa/`

---

## 🎯 Étape 2 : Lancer le setup (3 minutes)

### Sur Windows (PowerShell)
```bash
.\setup.ps1
```

### Sur Mac/Linux (Bash)
```bash
chmod +x setup.sh
./setup.sh
```

**Qu'est-ce qui se passe?**
1. Crée un `venv/` (environnement isolé)
2. Installe les librairies de `requirements.txt`
3. Crée un fichier `.env` (configuration)

**Résultat:** Prompt change en `(lisa) >` 

---

## 🔑 Étape 3 : Configurer les credentials Azure (2 minutes)

### Ouvre le fichier `.env`
```
.env
```

### Édite avec un éditeur (VS Code, Notepad, etc.)
```bash
AZURE_OPENAI_ENDPOINT=https://...
AZURE_OPENAI_API_KEY=sk-...
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-5.4-mini
```

### Demande les valeurs à un senior !
```
"Yo! Je dois les credentials Azure pour démarrer"
```

**Résultat:** `.env` est rempli avec les vraies valeurs

---

## ✅ Étape 4 : Lancer l'app (1 minute)

```bash
python main.py
```

**Résultat:**
```
======================================================================
  🏦 AGENT LISA DEMO - Setup Script
  LS V3.8.0 Loan Servicing System
======================================================================

Initialisation de l'Agent Data...
✓ Agent initialisé avec succès

TESTS RAPIDES
======================================================================

[USER] Combien de dossiers actifs avons-nous?

[AGENT] Nous avons **2 dossiers actifs**.
----------------------------------------------------------------------
```

---

## 💬 Étape 5 : Poser une question! (Maintenant!)

Dès que tu vois `[Vous] >`, tu peux taper:

```
[Vous] > Combien de dossiers actifs avons-nous?
```

**Réponse attendue:**
```
[AGENT] Nous avons **2 dossiers actifs**.
```

### Essaie d'autres questions:
```
[Vous] > Quel est le montant total accordé?
[VOUS] > Quels sont les événements récents?
[Vous] > Quel est le type de prêt du dossier LS-2024-001?
```

---

## 🎉 Bravo! Ça marche!

Tu viens de:
✅ Cloner le repo  
✅ Installer les dépendances  
✅ Configurer Azure  
✅ Lancer l'app  
✅ Poser une question à l'IA  

---

## 📚 Maintenant, apprends le code

### Étape 1 : Lis Python basics (5 min)
```
Ouvre: PYTHON_BASICS.md
```

### Étape 2 : Comprends l'architecture
```
Ouvre: JUNIOR_GUIDE.md (section Architecture)
```

### Étape 3 : Explore le code
```
Ouvre: src/agent/agent_data.py
Lis les comments (# ...)
Essaie de comprendre chaque fonction
```

### Étape 4 : Modifie le code
```python
# Dans main.py, ajoute une question personnalisée:
test_queries = [
    "Combien de dossiers actifs avons-nous?",
    "Quel est le montant total accordé?",
    "MA QUESTION ICI!"  # ← Ajoute la tienne!
]
```

---

## 🐛 Ça ne marche pas? (Troubleshooting)

### "Erreur: Python not found"
```bash
# Vérifie que Python est installé
python --version

# Sinon télécharge-le:
# https://www.python.org/downloads/
```

### "Erreur: module not found (openai, etc)"
```bash
# Tu dois installer les dépendances
pip install -r requirements.txt
```

### "Erreur: AZURE_OPENAI_ENDPOINT not set"
```bash
# Tu n'as pas rempli le .env
# Ouvre .env et ajoute les credentials
```

### "Erreur: (venv) prompt doesn't appear"
```bash
# Le venv n'est pas activé
# Windows:  .\venv\Scripts\Activate
# Mac:      source venv/bin/activate
```

### "Le LLM Azure ne répond pas"
```bash
# Vérifies le .env:
# - AZURE_OPENAI_ENDPOINT correct?
# - AZURE_OPENAI_API_KEY correct?
# - AZURE_OPENAI_DEPLOYMENT_NAME = gpt-5.4-mini?

# Teste:
python scripts/test_azure_setup.py
```

### "Je vois des questions de test mais je veux interactif"
```bash
# Laisse le script de test finir
# Puis ça devient interactif!
# Tape ta question quand tu vois [Vous] >
```

---

## 📁 Structure rapide

```
lisa/                          ← Tu es ici après git clone
├── main.py                    ← Lance ça! (python main.py)
├── .env                       ← Remplis ça avec credentials
├── src/
│   ├── agent/
│   │   ├── agent_data.py     ← Classe principale (lis ça après)
│   │   └── data_loader.py    ← Charge les données
│   ├── data/                 ← Fichiers JSON (dossiers, payeurs, événements)
│   └── config/               ← Configurations
├── docs/                      ← Documentation technique
├── README.md                  ← Vue générale
├── PYTHON_BASICS.md          ← Lis ça d'abord! (si zéro Python)
├── JUNIOR_GUIDE.md           ← Lis ça ensuite (architecture)
└── requirements.txt           ← Dépendances (pip install)
```

---

## ✅ Checklist pour les 30 prochaines minutes

- [ ] Cloner le repo (`git clone`)
- [ ] Lancer setup (`.\setup.ps1` ou `./setup.sh`)
- [ ] Remplir `.env` avec credentials Azure
- [ ] Lancer l'app (`python main.py`)
- [ ] Poser 3 questions différentes
- [ ] Lire PYTHON_BASICS.md (5 min)
- [ ] Lancer `python scripts/test_demo_ls_v3.py` (voir les données)
- [ ] Ouvrir `src/agent/agent_data.py` et lire les commentaires

---

## 🎓 Ressources

| Fichier | Pourquoi | Quand lire |
|---------|---------|----------|
| **PYTHON_BASICS.md** | Comprendre la syntaxe Python | Après clone, avant de coder |
| **JUNIOR_GUIDE.md** | Architecture détaillée | Après que ça marche |
| **STRUCTURE.md** | Organisation du projet | Pour naviguer le code |
| **README.md** | Vue générale complète | Après lancé l'app |
| **docs/** | Documentation technique LS V3.8.0 | Si tu dois modifier les données |

---

## 💬 Questions fréquentes démarreur

**Q: Pourquoi `./setup.ps1` ne fonctionne pas?**
A: Tu dois utiliser PowerShell (pas cmd.exe). Va en bas à droite → sélectionne PowerShell

**Q: Le script est resté sur "Mode Conversation"?**
A: C'est normal! Tape ta question: `[Vous] > Combien de dossiers?`

**Q: Il me demande `[Vous] >` mais rien ne s'affiche**
A: Il attend que tu tapes une question. Tape: `"Bonjour"` et appuie sur Entrée

**Q: Qu'est-ce qu'un `.env`?**
A: Fichier qui contient les secrets (clés API) sans les committer à Git

**Q: À quoi sert `requirements.txt`?**
A: Liste toutes les librairies Python nécessaires (comme pom.xml en Java)

**Q: Je dois modifier le code où?**
A: Dans `src/agent/` (sauf si tu sais ce que tu fais)

**Q: Comment je commit mon code?**
A: 
```bash
git add .
git commit -m "Ma description"
git push origin main
```

---

## 🎯 Objectif atteint?

✅ Tu as l'app qui marche  
✅ Tu peux poser des questions  
✅ Tu comprends la structure basique  
✅ Tu sais où modifier le code  

**Bravo! Bienvenue dans l'équipe! 🚀**

---

**Version**: 1.0  
**Date**: 2026-09-24  
**Pour**: Démarrage ASAP
