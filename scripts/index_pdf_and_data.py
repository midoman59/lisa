#!/usr/bin/env python3
"""
Ingest PDF documentation + JSON data into Azure Search with embeddings and intelligent chunking.
Based on expert colleague's rag_search implementation with API Key authentication.

Launch: python scripts/index_pdf_and_data.py
"""

import hashlib
import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Iterable, Iterator

from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader

load_dotenv()

# Configuration
CHUNK_SIZE = 1_000
CHUNK_OVERLAP = 150
EMBEDDING_DIMENSIONS = 1_536

# Environment variables
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_EMBEDDING_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small")
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT", "").rstrip("/")
AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")
AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX_NAME", "lisa-documents")

if not all([AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_API_KEY]):
    print("❌ Erreur: Manque de variables d'environnement")
    print("   Vérifie .env: AZURE_OPENAI_*, AZURE_SEARCH_*")
    exit(1)


def chunks(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> Iterator[str]:
    """Split text into overlapping chunks, preferring word boundaries."""
    text = re.sub(r"\s+", " ", text).strip()
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):
            boundary = text.rfind(" ", start, end)
            if boundary > start:
                end = boundary
        chunk = text[start:end].strip()
        if chunk:
            yield chunk
        if end == len(text):
            break
        start = max(end - overlap, start + 1)


def extract_pdf(path: Path) -> Iterable[tuple[str, dict[str, object]]]:
    """Extract text from PDF pages."""
    reader = PdfReader(path)
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            yield text, {"page": page_number}


def extract_json(path: Path) -> Iterable[tuple[str, dict[str, object]]]:
    """Extract structured data from JSON files."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    items = data if isinstance(data, list) else [data]
    for row_number, item in enumerate(items, start=1):
        text = json.dumps(item, ensure_ascii=False, indent=2)
        yield text, {"sheet": path.stem, "row_number": row_number}


def get_openai_client() -> tuple[OpenAI, str]:
    """Get OpenAI client configured for Azure."""
    endpoint = AZURE_OPENAI_ENDPOINT
    if "/api/projects/" in endpoint:
        endpoint = endpoint.split("/api/projects/", 1)[0]
    if not endpoint.endswith("/openai/v1"):
        endpoint = f"{endpoint}/openai/v1"

    return OpenAI(base_url=endpoint, api_key=AZURE_OPENAI_API_KEY), AZURE_OPENAI_EMBEDDING_DEPLOYMENT


def embed(client: OpenAI, deployment: str, text: str) -> list[float]:
    """Create embedding for text."""
    return client.embeddings.create(model=deployment, input=text).data[0].embedding


def request_search(method: str, url: str, api_key: str, payload: object | None = None) -> dict:
    """Make authenticated request to Azure Search."""
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        url,
        data=body,
        method=method,
        headers={"Content-Type": "application/json", "api-key": api_key},
    )
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8")) if response.length != 0 else {}
    except urllib.error.HTTPError as error:
        message = error.read().decode("utf-8")
        raise RuntimeError(f"Azure Search {method} {url} failed: {message}") from error


def ensure_index(endpoint: str, api_key: str, index_name: str) -> None:
    """Create or update Azure Search index with vector search configuration."""
    url = f"{endpoint}/indexes/{index_name}?api-version=2024-07-01"
    index = {
        "name": index_name,
        "fields": [
            {"name": "id", "type": "Edm.String", "key": True, "filterable": True},
            {"name": "content", "type": "Edm.String", "searchable": True},
            {"name": "content_vector", "type": "Collection(Edm.Single)", "searchable": True, "vectorSearchProfile": "vector-profile", "dimensions": EMBEDDING_DIMENSIONS},
            {"name": "source", "type": "Edm.String", "filterable": True, "facetable": True},
            {"name": "source_type", "type": "Edm.String", "filterable": True, "facetable": True},
            {"name": "page", "type": "Edm.Int32", "filterable": True, "sortable": True},
            {"name": "sheet", "type": "Edm.String", "filterable": True},
            {"name": "row_number", "type": "Edm.Int32", "filterable": True},
            {"name": "chunk_number", "type": "Edm.Int32", "filterable": True, "sortable": True},
        ],
        "vectorSearch": {
            "algorithms": [{"name": "hnsw", "kind": "hnsw", "hnswParameters": {"metric": "cosine"}}],
            "profiles": [{"name": "vector-profile", "algorithm": "hnsw"}],
        },
    }
    request_search("PUT", url, api_key, index)
    print(f"✅ Index '{index_name}' ready")


def ingest_documents(folder: Path) -> int:
    """Ingest PDF and JSON documents into Azure Search."""
    print("=" * 70)
    print("📚 INDEXATION INTELLIGENTE: PDF + JSON → AZURE SEARCH")
    print("=" * 70)

    client, embedding_deployment = get_openai_client()
    print(f"\n🔐 Configuration:")
    print(f"   Endpoint Search: {AZURE_SEARCH_ENDPOINT}")
    print(f"   Index: {AZURE_SEARCH_INDEX}")
    print(f"   Embedding: {embedding_deployment}")

    ensure_index(AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_API_KEY, AZURE_SEARCH_INDEX)

    documents = []

    # Process PDF
    pdf_path = Path("docs/LS_V3.8.0_Fichiers_Permanents.pdf")
    if pdf_path.exists():
        print(f"\n📄 Traitement PDF: {pdf_path.name}")
        for text, metadata in extract_pdf(pdf_path):
            for chunk_number, content in enumerate(chunks(text), start=1):
                identity = f"{pdf_path.resolve()}:{metadata}:{chunk_number}"
                print(f"   ⏳ Embedding chunk {chunk_number}...", end="\r")
                documents.append({
                    "@search.action": "mergeOrUpload",
                    "id": hashlib.sha256(identity.encode("utf-8")).hexdigest(),
                    "content": content,
                    "content_vector": embed(client, embedding_deployment, content),
                    "source": pdf_path.name,
                    "source_type": "pdf",
                    "page": metadata.get("page"),
                    "sheet": None,
                    "row_number": None,
                    "chunk_number": chunk_number,
                })
        print(f"   ✅ PDF: {len([d for d in documents if d['source_type'] == 'pdf'])} chunks\n")

    # Process JSON files
    json_files = [
        ("src/data/dossiers.json", "dossier"),
        ("src/data/enregistrements.json", "enregistrement"),
    ]

    for json_path, doc_type in json_files:
        path = Path(json_path)
        if not path.exists():
            print(f"   ⚠️  Fichier non trouvé: {json_path}")
            continue

        print(f"   📋 Traitement JSON: {path.name}")
        for text, metadata in extract_json(path):
            for chunk_number, content in enumerate(chunks(text), start=1):
                identity = f"{path.resolve()}:{metadata}:{chunk_number}"
                documents.append({
                    "@search.action": "mergeOrUpload",
                    "id": hashlib.sha256(identity.encode("utf-8")).hexdigest(),
                    "content": content,
                    "content_vector": embed(client, embedding_deployment, content),
                    "source": path.name,
                    "source_type": "json",
                    "page": None,
                    "sheet": metadata.get("sheet"),
                    "row_number": metadata.get("row_number"),
                    "chunk_number": chunk_number,
                })
        print(f"   ✅ {path.name}: chunks indexés")

    # Upload in batches
    if documents:
        print(f"\n📤 Upload de {len(documents)} documents...")
        url = f"{AZURE_SEARCH_ENDPOINT}/indexes/{AZURE_SEARCH_INDEX}/docs/index?api-version=2024-07-01"

        for start in range(0, len(documents), 100):
            batch = documents[start:start + 100]
            result = request_search("POST", url, AZURE_SEARCH_API_KEY, {"value": batch})
            failures = [item for item in result.get("value", []) if not item.get("status")]
            if failures:
                raise RuntimeError(f"Failed to index documents: {failures}")
            print(f"   ✅ {min(start + len(batch), len(documents))}/{len(documents)} documents indexés")

    print("\n" + "=" * 70)
    print(f"✅ INDEXATION TERMINÉE: {len(documents)} documents")
    print("=" * 70)
    return len(documents)


if __name__ == "__main__":
    ingest_documents(Path("."))
