#!/usr/bin/env python3
"""
Agent Data - Interroge les données sur les dossiers, enregistrements, événements
"""

import os
import json
from dotenv import load_dotenv
from .rag_loader import RAGLoader
from openai import AzureOpenAI

# Load environment
load_dotenv()

class DataAgent:
    """Agent qui interroge les données locales et utilise le LLM pour répondre"""

    def __init__(self):
        self.loader = RAGLoader()
        self.field_descriptions = self._load_field_descriptions()

        # Initialize Azure OpenAI client
        self.client = AzureOpenAI(
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2025-04-01-preview"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY")
        )
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-5.4-mini")

    def _load_field_descriptions(self) -> dict:
        """Charge le dictionnaire des descriptions de champs LS V3.8.0"""
        try:
            with open("field_descriptions.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _get_context(self, query: str) -> str:
        """Prépare le contexte basé sur RAG (PDF + données indexées dans Azure Search)"""
        context = "CONTEXTE RAG - LS V3.8.0 (PDF + DONNÉES):\n"
        context += "=" * 60 + "\n"

        # Récupérer les résultats du RAG (top 5 documents pertinents)
        rag_results = self.loader.search_documents(query, top=5)

        if rag_results:
            context += "\n📚 DOCUMENTS TROUVÉS (via RAG - Hybrid Search):\n"
            for i, doc in enumerate(rag_results, 1):
                source_info = f"{doc['source']}"
                if doc.get('page'):
                    source_info += f" (Page {doc['page']})"
                elif doc.get('sheet'):
                    source_info += f" ({doc['sheet']} Row {doc['row_number']})"

                context += f"\n{i}. {source_info}\n"
                context += f"   Type: {doc.get('source_type', 'unknown')} | Score: {doc['score']:.3f}\n"
                # Limiter le contenu pour ne pas surcharger le prompt
                content = doc['content'][:400]
                context += f"   {content}{'...' if len(doc['content']) > 400 else ''}\n"
        else:
            context += "\n⚠️  Aucun document trouvé dans le RAG\n"

        # Ajouter le dictionnaire des champs si disponible
        if self.field_descriptions:
            context += "\n" + "=" * 60 + "\n"
            context += "🔍 DICTIONNAIRE LS V3.8.0 (pour contexte supplémentaire):\n"

            dgen_count = len(self.field_descriptions.get("dgen", {}))
            dpay_count = len(self.field_descriptions.get("dpay", {}))
            dgar_count = len(self.field_descriptions.get("dgar", {}))

            context += f"  • DGEN: {dgen_count} champs\n"
            context += f"  • DPAY: {dpay_count} champs\n"
            context += f"  • DGAR: {dgar_count} champs\n"

        context += "\n" + "=" * 60 + "\n"
        return context

    def query(self, user_query: str) -> str:
        """Traite une requête utilisateur"""
        print(f"\n[USER] {user_query}")

        # Préparer le contexte
        context = self._get_context(user_query)

        # Appeler le LLM
        system_prompt = """Tu es un agent expert en gestion de dossiers de prêt bancaire (système Lisa).
Tu as accès à une base de données locale avec des dossiers, enregistrements et événements.
Tu dois répondre aux questions en te basant sur les données fournies.

Réponse en français, sois précis et concis."""

        try:
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "system", "content": f"CONTEXTE:\n{context}"},
                    {"role": "user", "content": user_query}
                ],
                temperature=0.7,
                max_completion_tokens=500
            )

            answer = response.choices[0].message.content
            print(f"\n[AGENT] {answer}")
            return answer

        except Exception as e:
            error_msg = f"Erreur LLM: {str(e)}"
            print(f"\n[AGENT] {error_msg}")
            return error_msg

    def chat(self):
        """Mode conversation interactif"""
        print("=" * 70)
        print("AGENT DATA - Mode Conversation")
        print("=" * 70)
        print("Posez vos questions sur les dossiers, enregistrements, événements")
        print("Tapez 'quit' pour quitter")
        print("=" * 70)

        while True:
            try:
                user_input = input("\n[Vous] > ").strip()
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Au revoir!")
                    break
                if not user_input:
                    continue

                self.query(user_input)
            except KeyboardInterrupt:
                print("\n\nAu revoir!")
                break


def main():
    """Point d'entrée"""
    print("Initialisation de l'Agent Data...")

    try:
        agent = DataAgent()
        print("✓ Agent initialisé avec succès")

        # Quelques requêtes de test
        test_queries = [
            "Combien de dossiers actifs avons-nous?",
            "Quel est le statut du dossier LS-2024-001?",
            "Quels sont les événements récents?",
            "Quel est le montant total accordé?",
        ]

        print("\n" + "=" * 70)
        print("TESTS RAPIDES")
        print("=" * 70)

        for query in test_queries:
            agent.query(query)
            print("-" * 70)

        # Mode interactif
        print("\n" + "=" * 70)
        print("Passons en mode conversation...")
        print("=" * 70)
        agent.chat()

    except Exception as e:
        print(f"✗ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
