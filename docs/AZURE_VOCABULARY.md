# 📚 Vocabulaire Azure - Explications Complètes

## 🏗️ Hiérarchie Azure (du plus large au plus petit)

```
┌─────────────────────────────────────────────────────────────┐
│ ORGANIZATION (Votre entreprise: SG)                         │
│ - Paie pour Azure                                           │
│ - Gère l'accès                                              │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│ TENANT (Répertoire Azure AD)                                │
│ - "AZURE SBX" (votre tenant dans cet environnement)        │
│ - Identifie tous les utilisateurs, groupes, applications    │
│ - Tenant ID: 51564ad7-13b1-44b0-8919-cd080a1b0e31         │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│ SUBSCRIPTION (Votre "compte de facturation")                │
│ - "hackathon" (Subscription ID: cd42c6a9-be39-499b-9cda...)│
│ - C'est où vos ressources vivent et où on paye              │
│ - Une organisation peut avoir plusieurs subscriptions       │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│ RESOURCE GROUPS (Conteneurs logiques)                       │
│ - "rg-uc25-assistant-lisa-creditme"                        │
│ - Regroupe les ressources par projet/team                   │
│ - Facilite la gestion et la facturation                     │
│ - Vous pouvez avoir 10+ resource groups par subscription   │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│ RESOURCES (Les services concrets)                           │
│ - Cognitive Services (AI Foundry)                           │
│ - Storage Accounts                                          │
│ - Databases                                                 │
│ - etc.                                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔑 Termes Clés Expliqués

### 1️⃣ **TENANT**
**Qu'est-ce que c'est ?**
- C'est votre répertoire Azure Active Directory (Azure AD)
- Contient tous vos utilisateurs, groupes, et permissions
- Chaque organisation a 1 ou plusieurs tenants

**Votre cas :**
```
Tenant Name:    AZURE SBX
Tenant ID:      51564ad7-13b1-44b0-8919-cd080a1b0e31
Domain:         sgazuresbx.onmicrosoft.com
```

**Analogie :** C'est comme votre "maison" Azure - tout ce qui est dedans appartient à ce tenant.

---

### 2️⃣ **SUBSCRIPTION**
**Qu'est-ce que c'est ?**
- C'est votre "compte de facturation" Azure
- Définit un budget, un scope de facturation
- Les ressources sont créées DANS une subscription

**Votre cas :**
```
Name:           hackathon
ID:             cd42c6a9-be39-499b-9cda-34d4cee517ab
State:          Enabled
Tenant ID:      51564ad7-13b1-44b0-8919-cd080a1b0e31
```

**Analogie :** C'est votre "portefeuille" - l'argent sort de là pour payer les services.

**Différence Tenant vs Subscription :**
- **Tenant** = Qui vous êtes (identité Azure AD)
- **Subscription** = Votre compte de facturation (où payer)
- Même si vous changez de subscription, vous restez le même tenant

---

### 3️⃣ **RESOURCE GROUP (RG)**
**Qu'est-ce que c'est ?**
- C'est un conteneur logique qui regroupe des ressources liées
- Les ressources dans un RG partent toutes en même temps quand on supprime le RG
- Facilite la gestion par projet ou équipe

**Votre cas :**
```
Resource Group:  rg-uc25-assistant-lisa-creditme
Location:        swedencentral / northeurope
Créateur:        Dimitrina
Projet:          Lisa CreditMe (assistant IA pour crédit)
```

**Nomenclature :** `rg-[usecase]-[project]`
- `rg` = Resource Group
- `uc25` = Use Case 25
- `assistant-lisa-creditme` = Projet spécifique

---

### 4️⃣ **COGNITIVE SERVICES / AI FOUNDRY**
**Qu'est-ce que c'est ?**
- Service Azure pour accéder aux modèles LLM (ChatGPT, GPT-4, etc.)
- Fournit une API REST/SDK pour faire des appels LLM
- On l'appelle aussi "AI Foundry" ou "Azure OpenAI Service"

**Votre cas :**
```
Resource Name:   lisa-creditme
Resource Type:   Microsoft.CognitiveServices/accounts
Location:        northeurope
Endpoint:        https://lisa-creditme.cognitiveservices.azure.com/
```

**Qu'est-ce qu'un "endpoint" ?**
- C'est l'adresse URL où vous faites vos requêtes LLM
- Format: `https://[NOM].cognitiveservices.azure.com/`
- C'est ce qu'on va mettre dans `AZURE_OPENAI_ENDPOINT` dans le .env

---

### 5️⃣ **PROJECT (dans Cognitive Services)**
**Qu'est-ce que c'est ?**
- C'est un sous-conteneur dans une ressource Cognitive Services
- Permet d'organiser plusieurs déploiements LLM dans la même ressource
- Structure: `[Resource]/[Project]`

**Votre cas :**
```
Resource:   lisa-creditme
Project:    lisa-creditme
Structure:  lisa-creditme/lisa-creditme
```

**Analogie :** Si Cognitive Services est un "bâtiment", un Project est un "bureau" dedans.

---

### 6️⃣ **DEPLOYMENT (Modèle LLM)**
**Qu'est-ce que c'est ?**
- C'est l'allocation d'une instance d'un modèle LLM (ex: gpt-4o-mini)
- Chaque deployment a un nom unique dans le projet
- On spécifie le modèle, la capacité (tokens/min), etc.

**Vous pouvez avoir :**
```
Project: lisa-creditme/lisa-creditme
  ├── Deployment 1: gpt-4o-mini (4K tokens/min)
  ├── Deployment 2: gpt-4 (2K tokens/min)
  └── Deployment 3: text-embedding (1K tokens/min)
```

**Dans le code, vous referencer le deployment :**
```python
from openai import AzureOpenAI

client = AzureOpenAI(
    api_version="2025-04-01-preview",
    azure_endpoint="https://lisa-creditme.cognitiveservices.azure.com/",
    # Vous spécifiez LE deployment à utiliser:
)

response = client.chat.completions.create(
    model="gpt-4o-mini",  # Nom du deployment
    messages=[...],
)
```

---

### 7️⃣ **AZURE CLI**
**Qu'est-ce que c'est ?**
- Ligne de commande pour gérer toutes les ressources Azure
- Alternative graphique = Azure Portal (web)

**Commandes principales qu'on a utilisées :**
```bash
az login                    # Se connecter
az account show             # Voir votre subscription
az resource list            # Lister toutes les ressources
az cognitiveservices account show  # Voir les détails d'une ressource
```

---

### 8️⃣ **API VERSION**
**Qu'est-ce que c'est ?**
- La version de l'API Azure OpenAI que vous utilisez
- Elle change régulièrement pour de nouvelles features
- Format: `YYYY-MM-DD-preview` ou `YYYY-MM-DD`

**Votre cas :**
```
AZURE_OPENAI_API_VERSION=2025-04-01-preview
```

**Où trouver les versions :** https://learn.microsoft.com/en-us/azure/ai-services/openai/reference

---

## 🔐 Authentication : Les 2 Méthodes

### Méthode 1 : Azure CLI (Recommandée pour dev)
```bash
az login  # Vous vous loggez une fois
# Azure CLI garde votre session en mémoire
# Les SDKs utilisent cette session automatiquement
```

**Avantage :** Sécurisé, pas de clés en hard-code
**Désavantage :** Fonctionne seulement quand Azure CLI est installé

### Méthode 2 : API Keys (Pour prod / automation)
```python
# Stocker dans .env (JAMAIS en hard-code)
AZURE_OPENAI_API_KEY=sk-...
```

**Avantage :** Fonctionne partout
**Désavantage :** Moins sécurisé, clés à protéger

**Votre cas :** On utilise la Méthode 1 (Azure CLI), c'est plus sûr pour le dev.

---

## 📝 Exemple : Comprendre Votre Setup Actuel

```
┌─ TENANT: AZURE SBX (sgazuresbx.onmicrosoft.com)
│  └─ SUBSCRIPTION: hackathon (cd42c6a9-be39-499b...)
│     └─ RESOURCE GROUP: rg-uc25-assistant-lisa-creditme
│        └─ COGNITIVE SERVICE: lisa-creditme
│           ├─ Endpoint: https://lisa-creditme.cognitiveservices.azure.com/
│           └─ PROJECT: lisa-creditme
│              └─ DEPLOYMENT: gpt-4o-mini (probablement)
│
│  └─ SUBSCRIPTION: hackathon
│     └─ RESOURCE GROUP: rg-hackathon-rbs2026-adam
│        └─ COGNITIVE SERVICE: foundry-hackathon-rbs2026-adam
│           (Exemple par Adam, on ignore celui-ci)
```

---

## 🎯 Ce Que Vous Utiliserez

Pour le chatbot hackathon, vous aurez besoin de :

| Élément | Valeur |
|---------|--------|
| **Tenant** | AZURE SBX |
| **Subscription** | hackathon |
| **Resource Group** | rg-uc25-assistant-lisa-creditme |
| **Cognitive Service** | lisa-creditme |
| **Endpoint** | `https://lisa-creditme.cognitiveservices.azure.com/` |
| **Project** | lisa-creditme |
| **API Version** | 2025-04-01-preview |
| **Auth Method** | Azure CLI (`az login`) |

---

## 🚀 Prochaines Étapes

1. **Récupérer la clé API** (optionnel, pour backup)
   ```bash
   az cognitiveservices account keys list \
     --name lisa-creditme \
     --resource-group rg-uc25-assistant-lisa-creditme
   ```

2. **Créer le `.env`** avec vos valeurs

3. **Créer le test script** pour vérifier la connexion

4. **Tester la connexion** avec un appel simple au LLM

---

**Des questions sur ces concepts ?** Pose-les avant qu'on continue ! 👇
