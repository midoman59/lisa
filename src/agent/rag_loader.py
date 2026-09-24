#!/usr/bin/env python3
"""
RAG Loader - Recherche dans Azure Search (PDF + Data indexées)
"""

import os
from typing import List, Dict, Any
from azure.search.documents import SearchClient
from azure.identity import DefaultAzureCredential


class RAGLoader:
    """Charge les données via Azure Search RAG"""

    def __init__(self):
        """Initialise le client Azure Search"""
        self.endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        self.index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "lisa-documents")

        if not self.endpoint:
            raise ValueError("AZURE_SEARCH_ENDPOINT requis dans .env")

        # Utiliser DefaultAzureCredential pour Azure AD
        credential = DefaultAzureCredential()

        self.client = SearchClient(
            endpoint=self.endpoint,
            index_name=self.index_name,
            credential=credential
        )

        print(f"✓ RAGLoader initialisé")
        print(f"  Endpoint: {self.endpoint}")
        print(f"  Index: {self.index_name}")

    def search_documents(self, query: str, top: int = 5) -> List[Dict[str, Any]]:
        """
        Cherche les documents pertinents dans Azure Search

        Args:
            query: La requête utilisateur
            top: Nombre de résultats à retourner

        Returns:
            Liste des documents trouvés avec contenu et métadonnées
        """
        try:
            # Chercher par sémantique dans Azure Search
            results = self.client.search(
                search_text=query,
                top=top,
                select=["id", "content", "type", "document_id", "source", "metadata"]
            )

            documents = []
            for result in results:
                doc = {
                    "id": result.get("id", ""),
                    "content": result.get("content", ""),
                    "type": result.get("type", ""),
                    "document_id": result.get("document_id", ""),
                    "source": result.get("source", ""),
                    "metadata": result.get("metadata", ""),
                    "score": result.get("@search.score", 0.0),
                }
                documents.append(doc)

            return documents

        except Exception as e:
            print(f"⚠️  Erreur recherche: {e}")
            return []

    def get_context_string(self, query: str, top: int = 5) -> str:
        """
        Retourne les résultats formatés pour le contexte LLM

        Args:
            query: La requête utilisateur
            top: Nombre de résultats à retourner

        Returns:
            String formaté avec les résultats
        """
        results = self.search_documents(query, top)

        if not results:
            return "Aucun document trouvé dans la base de connaissances."

        context = "RÉSULTATS DE LA RECHERCHE RAG:\n"
        context += "=" * 60 + "\n"

        for i, doc in enumerate(results, 1):
            context += f"\n{i}. Source: {doc['source']} (Type: {doc['type']}, Score: {doc['score']:.2f})\n"
            context += f"   {doc['content'][:300]}{'...' if len(doc['content']) > 300 else ''}\n"

        context += "\n" + "=" * 60 + "\n"
        return context

    def get_statistics(self) -> Dict[str, Any]:
        """Retourne des stats sur l'index (optionnel)"""
        try:
            # Pour l'instant, retourner un dict vide
            # Azure Search n'expose pas directement les stats
            return {
                "endpoint": self.endpoint,
                "index": self.index_name,
                "status": "connected"
            }
        except:
            return {}


if __name__ == "__main__":
    # Test simple
    loader = RAGLoader()

    # Test query
    test_query = "dossiers actifs"
    print(f"\nTest: {test_query}")
    print("-" * 60)

    results = loader.search_documents(test_query, top=3)
    print(f"Résultats trouvés: {len(results)}")

    for r in results:
        print(f"\n  {r['source']} ({r['type']})")
        print(f"  {r['content'][:200]}...")
