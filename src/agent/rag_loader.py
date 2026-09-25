#!/usr/bin/env python3
"""
RAG Loader - Recherche intelligente dans Azure Search avec embeddings vectoriels.
Utilise API Key authentication et hybrid search (keyword + vector).
"""

import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

# Load .env from project root
load_dotenv(Path(__file__).parent.parent.parent / ".env")


class RAGLoader:
    """Charge les données via Azure Search avec recherche vectorielle."""

    def __init__(self):
        """Initialise le client pour recherche RAG avec embeddings."""
        self.endpoint = os.getenv("AZURE_SEARCH_ENDPOINT", "").rstrip("/")
        self.api_key = os.getenv("AZURE_SEARCH_API_KEY")
        self.index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "lisa-documents")

        # OpenAI pour embeddings
        openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
        openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small")

        if not all([self.endpoint, self.api_key, openai_endpoint, openai_api_key]):
            raise ValueError("Configuration Azure manquante dans .env")

        # Configure OpenAI client
        base_url = openai_endpoint
        if "/api/projects/" in base_url:
            base_url = base_url.split("/api/projects/", 1)[0]
        if not base_url.endswith("/openai/v1"):
            base_url = f"{base_url}/openai/v1"

        self.openai_client = OpenAI(base_url=base_url, api_key=openai_api_key)
        self.embedding_deployment = embedding_deployment

        print(f"RAGLoader initialise (Hybrid Search)")
        print(f"  Endpoint: {self.endpoint}")
        print(f"  Index: {self.index_name}")

    def embed_text(self, text: str) -> list[float]:
        """Crée un embedding pour un texte."""
        return self.openai_client.embeddings.create(
            model=self.embedding_deployment,
            input=text
        ).data[0].embedding

    def search_documents(self, query: str, top: int = 5, filter_expr: str | None = None) -> list[dict[str, Any]]:
        """
        Recherche hybrid (keyword + vector) dans Azure Search.

        Args:
            query: La requête utilisateur
            top: Nombre de résultats à retourner
            filter_expr: Filtre OData optionnel (ex: "source eq 'field_codes.json'")

        Returns:
            Liste des documents trouvés avec score
        """
        try:
            # Créer embedding pour la requête
            query_vector = self.embed_text(query)

            # Préparer la requête hybrid avec format correct (vectorQueries, pas vectors)
            search_payload = {
                "search": query,
                "top": top,
                "select": "id,content,source,source_type,page,sheet,row_number,chunk_number",
                "vectorQueries": [
                    {
                        "kind": "vector",
                        "vector": query_vector,
                        "fields": "content_vector",
                        "k": top,
                    }
                ],
            }
            if filter_expr:
                search_payload["filter"] = filter_expr

            # Effectuer la recherche
            url = f"{self.endpoint}/indexes/{self.index_name}/docs/search?api-version=2024-07-01"
            result = self._request_search("POST", url, search_payload)

            documents = []
            for item in result.get("value", []):
                doc = {
                    "id": item.get("id", ""),
                    "content": item.get("content", ""),
                    "source": item.get("source", ""),
                    "source_type": item.get("source_type", ""),
                    "page": item.get("page"),
                    "sheet": item.get("sheet"),
                    "row_number": item.get("row_number"),
                    "chunk_number": item.get("chunk_number"),
                    "score": item.get("@search.score", 0.0),
                }
                documents.append(doc)

            return documents

        except Exception as e:
            print(f"Erreur recherche: {e}")
            return []

    def get_context_string(self, query: str, top: int = 5) -> str:
        """
        Formate les résultats pour le contexte LLM.

        Args:
            query: La requête utilisateur
            top: Nombre de résultats à retourner

        Returns:
            String formaté avec les résultats
        """
        results = self.search_documents(query, top)

        if not results:
            return "Aucun document trouvé dans la base de connaissances RAG."

        context = "📚 CONTEXTE RAG (Recherche Hybrid Keyword + Vector):\n"
        context += "=" * 70 + "\n\n"

        for i, doc in enumerate(results, 1):
            # Source info
            source_info = f"{doc['source']}"
            if doc['page']:
                source_info += f" (Page {doc['page']})"
            elif doc['sheet']:
                source_info += f" ({doc['sheet']} Row {doc['row_number']})"

            context += f"{i}. [{source_info}] Score: {doc['score']:.3f}\n"
            context += f"   {doc['content'][:400]}{'...' if len(doc['content']) > 400 else ''}\n\n"

        context += "=" * 70 + "\n"
        return context

    def get_statistics(self) -> dict[str, Any]:
        """Retourne des infos sur la connexion RAG."""
        return {
            "endpoint": self.endpoint,
            "index": self.index_name,
            "auth": "API Key",
            "search_type": "Hybrid (Keyword + Vector)",
            "status": "connected"
        }

    def _request_search(self, method: str, url: str, payload: Any = None) -> dict:
        """Effectue une requête authentifiée à Azure Search."""
        body = json.dumps(payload).encode("utf-8") if payload is not None else None
        request = urllib.request.Request(
            url,
            data=body,
            method=method,
            headers={"Content-Type": "application/json", "api-key": self.api_key},
        )
        try:
            with urllib.request.urlopen(request) as response:
                return json.loads(response.read().decode("utf-8")) if response.length != 0 else {}
        except urllib.error.HTTPError as error:
            message = error.read().decode("utf-8")
            raise RuntimeError(f"Azure Search {method} {url} failed: {message}") from error


if __name__ == "__main__":
    # Test simple
    loader = RAGLoader()

    test_query = "structure des dossiers de crédit"
    print(f"\nTest RAG: {test_query}")
    print("-" * 70)

    results = loader.search_documents(test_query, top=3)
    print(f"✓ Résultats trouvés: {len(results)}\n")

    for r in results:
        print(f"  {r['source']} (Score: {r['score']:.3f})")
        print(f"  {r['content'][:250]}...\n")
