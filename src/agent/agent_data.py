#!/usr/bin/env python3
"""
Agent Data - Interroge les données sur les dossiers, enregistrements, événements
"""

import os
import re
import json
from pathlib import Path
from dotenv import load_dotenv
from .rag_loader import RAGLoader
from .improved_data_lookup import ImprovedDataLookup
from openai import AzureOpenAI

# Load environment
load_dotenv()

# Un code de champ LS ressemble à CDSITDOS-22, TYDINC-22, DTMAJHB-50...
FIELD_CODE_RE = re.compile(r"\b[A-Z][A-Z0-9]{1,15}-\d{1,3}\b")

class DataAgent:
    """Agent qui interroge les données locales et utilise le LLM pour répondre"""

    def __init__(self):
        self.loader = RAGLoader()
        self.field_descriptions = self._load_field_descriptions()
        self.field_codes = self._load_field_codes()
        self.data_lookup = ImprovedDataLookup()

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

    def _load_field_codes(self) -> dict:
        """Charge field_codes.json (schéma complet) pour un lookup EXACT par code,
        indépendant de la recherche sémantique qui n'est pas fiable pour des
        identifiants exacts (ex: "et TYDINC-22" en langage naturel fait perdre
        le bon résultat au profit de faux positifs proches sémantiquement)."""
        path = Path(__file__).parent.parent.parent / "src" / "data" / "field_codes.json"
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _exact_code_lookup(self, query: str) -> str:
        """Cherche dans le texte de la question des codes de champs explicites
        (ex: CDSITDOS-22) et retourne leur définition EXACTE depuis field_codes.json,
        sans dépendre du score de similarité de la recherche vectorielle."""
        if not self.field_codes:
            return ""

        codes = set(FIELD_CODE_RE.findall(query.upper()))
        if not codes:
            return ""

        all_fields = self.field_codes.get("all_fields", {})
        field_values = self.field_codes.get("field_values", {})

        blocks = []
        for code in codes:
            occurrences = all_fields.get(code)
            if not occurrences:
                continue
            for occ in occurrences:
                table = occ.get("table")
                lines = [
                    f"Champ: {code}",
                    f"Table: {table}",
                    f"Enregistrement: {occ.get('enregistrement', '')}",
                    f"Type: {occ.get('type', '')}",
                    f"Description: {occ.get('description', '')}",
                ]
                values = field_values.get(table, {}).get(code)
                if values:
                    lines.append("Valeurs possibles:")
                    for val_code, val_desc in values.items():
                        lines.append(f"  {val_code} = {val_desc}")
                blocks.append("\n".join(lines))

        if not blocks:
            return ""

        return (
            "\n🎯 CORRESPONDANCE EXACTE (lookup direct dans le schéma, prioritaire "
            "sur la recherche RAG ci-dessous):\n" + "\n---\n".join(blocks) + "\n"
        )

    def _get_context(self, query: str) -> str:
        """Prépare le contexte basé sur RAG (PDF + données indexées dans Azure Search)"""
        context = "CONTEXTE RAG - LS V3.8.0 (PDF + DONNÉES):\n"
        context += "=" * 60 + "\n"

        # Lookup exact si la question mentionne un code de champ explicite
        exact_match = self._exact_code_lookup(query)
        if exact_match:
            context += exact_match

        # Lookup direct dans les données structurées (dpay, dgar, etc.)
        direct_data = self.data_lookup.format_context(query)
        if direct_data:
            context += direct_data

        # Recherche séparée schéma (field_codes.json) vs données mock (dossiers/
        # enregistrements/evenements). Un classement unique fait perdre les
        # données réelles: field_codes.json compte 34 documents qui répètent
        # "Table: DOSSIER" et des mots comme "événement" (ex: TYDINC-22), ce qui
        # les fait remonter avant les vrais enregistrements même à top=10.
        schema_results = self.loader.search_documents(
            query, top=5, filter_expr="source eq 'field_codes.json'"
        )
        # Le corpus mock (dossiers+enregistrements+evenements) ne fait que ~12
        # enregistrements au total: on les récupère tous plutôt que de risquer
        # d'en perdre par dilution sémantique (ex: "montant" apparaît dans
        # quasi tous les enregistrements, donc top=8 loupait parfois DOS001/DOS002).
        data_results = self.loader.search_documents(
            query, top=20, filter_expr="source ne 'field_codes.json'"
        )
        rag_results = data_results + schema_results

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

⚠️ RÈGLES STRICTES:
1. SEULE les données du CONTEXTE fourni sont valides
2. JAMAIS inventer de données, codes ou valeurs qui ne sont pas dans le CONTEXTE
3. Si tu vois des codes ou valeurs dans le CONTEXTE, cite-les EXACTEMENT sans les modifier
4. Si le CONTEXTE contient PLUSIEURS enregistrements pertinents (ex: plusieurs dossiers,
   événements), liste-les TOUS, pas seulement le premier
5. Tu PEUX additionner, compter ou agréger des valeurs numériques QUI SONT PRÉSENTES dans
   le CONTEXTE (ex: sommer les montants de plusieurs dossiers listés) - ce n'est pas de
   l'invention, juste un calcul sur des données réelles fournies
6. Seulement si AUCUNE donnée pertinente n'apparaît dans le CONTEXTE, réponds "Je ne trouve
   pas cette information dans la base de données"

Réponse en français, sois précis et concis."""

        try:
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "system", "content": f"CONTEXTE:\n{context}"},
                    {"role": "user", "content": user_query}
                ],
                temperature=0.1,  # TRÈS BAS: réponses précises basées sur le contexte (pas de créativité/hallucinations)
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
