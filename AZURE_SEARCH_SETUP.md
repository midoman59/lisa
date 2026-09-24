# Configuration Azure Search - Diag nostic

## Problème Actuel

```
RuntimeError: The given API key doesn't match service's internal, primary or secondary keys.
```

La clé `AZURE_SEARCH_API_KEY` dans `.env` n'est pas acceptée par Azure Search.

---

## Solution: Obtenir les Bonnes Clés

### Option 1: Azure CLI (Recommandé)

```bash
# Se connecter à Azure
az login

# Afficher les clés admin
az search admin-key show \
  --resource-group rg-uc25-assistant-lisa-creditme \
  --service-name lisa-creditme-srch-kwrn
```

### Option 2: Azure Portal

1. **Aller à**: Azure Portal → Recherche → `lisa-creditme-srch-kwrn`
2. **Menu de gauche**: `Keys` (Clés)
3. **Copier**:
   - `Primary admin key` → `AZURE_SEARCH_API_KEY` dans `.env`
   - Ou `Primary query key` → `AZURE_SEARCH_QUERY_KEY`

---

## Clés Disponibles

Azure Search fournit plusieurs types de clés:

| Type | Usage | Permissions |
|------|-------|-------------|
| **Admin Key** | Indexation, configuration | Lecture/Écriture complète |
| **Query Key** | Recherche uniquement | Lecture seule |

**Pour ce projet**: Utilise la **Primary Admin Key** (elle peut tout faire).

---

## Vérifier la Clé

Une fois la clé mise à jour dans `.env`:

```bash
# Test rapide
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv('AZURE_SEARCH_API_KEY')
endpoint = os.getenv('AZURE_SEARCH_ENDPOINT')
print(f'✅ Clé: {key[:10]}...' if key else '❌ Clé manquante')
print(f'✅ Endpoint: {endpoint}')
"
```

---

## Relancer l'Indexation

Après avoir mis à jour `.env`:

```bash
python scripts/index_pdf_and_data.py
```

Cela va:
1. ✅ Créer l'index Azure Search avec schéma RAG
2. ✅ Extraire le PDF (346 pages → ~1300 chunks)
3. ✅ Charger données JSON (6 documents)
4. ✅ Créer embeddings pour chaque chunk
5. ✅ Uploader par batch (100 docs à la fois)

---

## Données à Indexer

### 📄 PDF
- **Fichier**: `docs/LS_V3.8.0_Fichiers_Permanents.pdf`
- **Taille**: 3.6 MB, 346 pages
- **Contenu**: Schéma complet LS V3.8.0 (DGEN, DLIGN, DREV, etc.)
- **Chunks**: ~1300 fragments (1000 chars, 150 overlap)

### 📋 JSON
- **dossiers.json**: 3 documents
- **enregistrements.json**: 3 documents
- **événements.json**: (optionnel)
- **Chunks**: ~6-10 fragments par document

---

## Architecture RAG Refactorisée

```
┌─────────────────────────────────────┐
│  Agent Question                      │
└─────────────────┬───────────────────┘
                  │
                  ▼
      ┌──────────────────────┐
      │ RAGLoader.embed()    │
      │ (OpenAI embedding)   │
      └──────────────────────┘
                  │
                  ▼
      ┌──────────────────────────────────┐
      │ Azure Search Hybrid Search        │
      │ • Keyword search                 │
      │ • Vector search (embeddings)     │
      └──────────────────────────────────┘
                  │
                  ▼
      ┌──────────────────────┐
      │ Top 5 Results        │
      │ + Metadata & Scores  │
      └──────────────────────┘
                  │
                  ▼
      ┌──────────────────────┐
      │ Agent LLM Context    │
      │ (gpt-5.4-mini)       │
      └──────────────────────┘
```

---

## Prochaines Étapes

1. ✅ Obtenir clé API correcte
2. ✅ Mettre à jour `.env`
3. ✅ Lancer `scripts/index_pdf_and_data.py`
4. ✅ Tester `src/agent/rag_loader.py`
5. ✅ Tester l'agent complet

---

## Support

Si le problème persiste:
- Vérifie que la clé est copiée EXACTEMENT (pas d'espaces)
- Assure-toi d'utiliser une "Primary admin key" (pas query key)
- Réessaie après 1-2 minutes (cache Azure)
