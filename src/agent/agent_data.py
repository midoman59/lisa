#!/usr/bin/env python3
"""
Agent Data - Interroge les données sur les dossiers, enregistrements, événements
"""

import os
import json
from dotenv import load_dotenv
from .data_loader import DataLoader
from openai import AzureOpenAI

# Load environment
load_dotenv()

class DataAgent:
    """Agent qui interroge les données locales et utilise le LLM pour répondre"""

    def __init__(self):
        self.loader = DataLoader()
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
        """Prépare le contexte basé sur la requête avec descriptions LS V3.8.0"""
        context = "CONTEXTE DE DONNÉES LS V3.8.0 (Loan Servicing):\n"

        # Dictionnaire des descriptions de champs (pour contextualiser l'IA)
        if self.field_descriptions:
            context += "\n🔍 DICTIONNAIRE DES CHAMPS (LS V3.8.0):\n"
            context += "━" * 60 + "\n"
            context += "TABLE DGEN (Données Générales du Dossier):\n"
            for field, desc in self.field_descriptions.get("dgen", {}).items():
                context += f"  • {field}: {desc}\n"

            context += "\nTABLE DPAY (Données de Payeur):\n"
            for field, desc in self.field_descriptions.get("dpay", {}).items():
                context += f"  • {field}: {desc}\n"

            context += "\nTABLE DGAR (Données de Garanties):\n"
            for field, desc in self.field_descriptions.get("dgar", {}).items():
                context += f"  • {field}: {desc}\n"

            context += "\nSÉMANTIQUE & CODES (pour interpréter les valeurs):\n"
            for code, meaning in self.field_descriptions.get("contexte_semantique", {}).items():
                context += f"  • {code}: {meaning}\n"
            context += "━" * 60 + "\n"

        # Statistiques
        stats = self.loader.get_statistics()
        context += f"\n📊 STATISTIQUES:\n{json.dumps(stats, indent=2)}\n"

        # Dossiers correspondants avec structures LS V3.8.0
        dossiers = self.loader.search_dossiers(query)
        if dossiers:
            context += f"\n📋 DOSSIERS TROUVÉS (structures DGEN+DPAY+DGAR):\n"

            # Ajouter les détails complets pour les dossiers trouvés
            for d in dossiers:
                summary = self.loader.get_dossier_summary(d.get("id"))
                context += f"\nDossier: {d.get('numero_dossier')} (Client: {d.get('client_nom')})\n"
                context += json.dumps(summary, indent=2, default=str, ensure_ascii=False) + "\n"

        # Événements récents
        recents = self.loader.get_evenements_recents(5)
        context += f"\n📅 ÉVÉNEMENTS RÉCENTS:\n{json.dumps(recents, indent=2, ensure_ascii=False)}\n"

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
