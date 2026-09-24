#!/usr/bin/env python3
"""
Index PDF documentation + JSON data into Azure Search for RAG
Lance: python scripts/index_pdf_and_data.py
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.identity import DefaultAzureCredential

# Essayer d'importer pdfplumber, sinon PyPDF2
try:
    import pdfplumber
    PDF_READER = "pdfplumber"
except ImportError:
    try:
        from PyPDF2 import PdfReader
        PDF_READER = "PyPDF2"
    except ImportError:
        print("❌ Erreur: pdfplumber ou PyPDF2 requis")
        print("   Installe: pip install pdfplumber")
        exit(1)

load_dotenv()

# Configuration
ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
ADMIN_KEY = os.getenv("AZURE_SEARCH_ADMIN_KEY")
INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME", "lisa-documents")

if not ENDPOINT or not ADMIN_KEY:
    print("❌ Erreur: AZURE_SEARCH_ENDPOINT et AZURE_SEARCH_ADMIN_KEY requis dans .env")
    exit(1)

print("=" * 70)
print("📚 INDEXATION: PDF + DATA JSON → AZURE SEARCH")
print("=" * 70)

# Créer le client Search avec Admin Key
try:
    search_client = SearchClient(
        endpoint=ENDPOINT,
        index_name=INDEX_NAME,
        credential=AzureKeyCredential(ADMIN_KEY)
    )
    print("\n✅ Connexion à Azure Search établie")
    print(f"   Endpoint: {ENDPOINT}")
    print(f"   Index: {INDEX_NAME}")
except Exception as e:
    print(f"\n❌ Erreur connexion: {e}")
    exit(1)

# ========== INDEXER LE PDF ==========

PDF_PATH = Path("docs/LS_V3.8.0_Fichiers_Permanents.pdf")

if PDF_PATH.exists():
    print(f"\n📝 Étape 1: Extraire et indexer le PDF...")
    print(f"   Fichier: {PDF_PATH}")

    try:
        # Extraire le texte du PDF
        pdf_text = ""
        page_count = 0

        if PDF_READER == "pdfplumber":
            with pdfplumber.open(PDF_PATH) as pdf:
                page_count = len(pdf.pages)
                for i, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        pdf_text += f"\n--- Page {i+1} ---\n{page_text}"
        else:
            with open(PDF_PATH, "rb") as f:
                reader = PdfReader(f)
                page_count = len(reader.pages)
                for i, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        pdf_text += f"\n--- Page {i+1} ---\n{page_text}"

        print(f"   ✅ Extrait: {page_count} pages")

        # Diviser le contenu en chunks (1000 caractères par chunk)
        chunk_size = 1000
        chunks = []

        for i in range(0, len(pdf_text), chunk_size):
            chunk = pdf_text[i:i + chunk_size]
            chunks.append({
                "id": f"pdf-chunk-{len(chunks)}",
                "content": chunk,
                "type": "documentation",
                "document_id": "LS_V3.8.0",
                "source": "LS_V3.8.0_Fichiers_Permanents.pdf",
                "metadata": f"PDF Documentation - Page coverage"
            })

        # Indexer les chunks
        if chunks:
            print(f"   📤 Indexation de {len(chunks)} chunks du PDF...")
            search_client.upload_documents(chunks)
            print(f"   ✅ PDF indexé: {len(chunks)} chunks")
        else:
            print("   ⚠️  Aucun contenu extrait du PDF")

    except Exception as e:
        print(f"   ❌ Erreur traitement PDF: {e}")
        print("   💡 Installe: pip install pdfplumber")
else:
    print(f"\n⚠️  PDF non trouvé: {PDF_PATH}")

# ========== INDEXER LES DONNÉES JSON ==========

print(f"\n📝 Étape 2: Indexer les données JSON...")

json_files = [
    ("src/data/dossiers.json", "dossier"),
    ("src/data/enregistrements.json", "enregistrement"),
    ("src/data/événements.json", "événement"),
]

documents_to_index = []

for json_path, doc_type in json_files:
    json_file = Path(json_path)

    if not json_file.exists():
        print(f"   ⚠️  Fichier non trouvé: {json_path}")
        continue

    print(f"   📂 Lecture: {json_path}")

    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Gérer si c'est une liste ou un dict
        items = data if isinstance(data, list) else [data]

        for i, item in enumerate(items):
            # Créer une représentation textuelle du document
            content = json.dumps(item, ensure_ascii=False, indent=2)
            doc_id = item.get("id") or item.get("numero_dossier") or f"{doc_type}-{i}"

            doc = {
                "id": f"{doc_type}-{doc_id}",
                "content": content,
                "type": doc_type,
                "document_id": str(doc_id),
                "source": json_file.name,
                "metadata": json.dumps({
                    "file": json_file.name,
                    "type": doc_type,
                    **{k: v for k, v in item.items() if isinstance(v, (str, int, float, bool))}
                }, ensure_ascii=False)
            }
            documents_to_index.append(doc)

        print(f"      ✅ {len(items)} documents lus")

    except Exception as e:
        print(f"      ❌ Erreur: {e}")

# Indexer tous les documents
if documents_to_index:
    print(f"\n   📤 Indexation de {len(documents_to_index)} documents JSON...")
    try:
        search_client.upload_documents(documents_to_index)
        print(f"   ✅ Données JSON indexées: {len(documents_to_index)} documents")
    except Exception as e:
        print(f"   ❌ Erreur indexation: {e}")

# ========== RÉSUMÉ ==========

print("\n" + "=" * 70)
print("✅ INDEXATION TERMINÉE!")
print("=" * 70)

total_docs = len(chunks) + len(documents_to_index) if PDF_PATH.exists() else len(documents_to_index)

print(f"""
📊 Résumé:
   - PDF: {len(chunks) if PDF_PATH.exists() else 0} chunks indexés
   - JSON: {len(documents_to_index)} documents indexés
   - Total: {total_docs} documents dans Azure Search

✅ Le RAG peut maintenant:
   - Répondre sur la structure LS V3.8.0 (depuis PDF)
   - Répondre sur les données actuelles (depuis JSON)
   - Combiner contexte PDF + données pour réponses intelligentes

🚀 Test: python main.py
""")
