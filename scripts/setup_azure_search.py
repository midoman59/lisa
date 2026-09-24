#!/usr/bin/env python3
"""
Setup Azure Search for RAG - Récupère les credentials du service existant
"""

import os
import json
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
)
from azure.mgmt.search import SearchManagementClient
from azure.identity import DefaultAzureCredential

load_dotenv()

SUBSCRIPTION_ID = "cd42c6a9-be39-499b-9cda-34d4cee517ab"
RESOURCE_GROUP = "rg-uc25-assistant-lisa-creditme"
SEARCH_SERVICE_NAME = "lisa-creditme-srch-kwrn"
INDEX_NAME = "lisa-documents"

print("=" * 70)
print("🔍 SETUP AZURE SEARCH POUR RAG")
print("=" * 70)

try:
    # Authentification
    credential = DefaultAzureCredential()
    print("\n✅ Authentification détectée")

    # Client de gestion
    mgmt_client = SearchManagementClient(credential, SUBSCRIPTION_ID)

    # Vérifier le service
    print(f"\n📝 Étape 1: Vérifier le service '{SEARCH_SERVICE_NAME}'...")
    service = mgmt_client.services.get(RESOURCE_GROUP, SEARCH_SERVICE_NAME)
    print(f"  ✅ Service trouvé")

    # Récupérer l'endpoint
    endpoint = f"https://{SEARCH_SERVICE_NAME}.search.windows.net"
    print(f"  Endpoint: {endpoint}")

    # Récupérer les admin keys
    print("\n📝 Étape 2: Récupérer les credentials...")
    admin_keys = mgmt_client.admin_keys.get(RESOURCE_GROUP, SEARCH_SERVICE_NAME)
    admin_key = admin_keys.primary_key
    print(f"  ✅ Admin Key récupérée")

    # Créer le client index (utiliser DefaultAzureCredential car DisableLocalAuth=True)
    print(f"\n📝 Étape 3: Vérifier/créer l'index '{INDEX_NAME}'...")
    index_client = SearchIndexClient(
        endpoint=endpoint,
        credential=credential  # Utiliser Azure AD au lieu de clés
    )

    # Définir les champs
    fields = [
        SimpleField(
            name="id",
            type=SearchFieldDataType.String,
            key=True,
            filterable=True,
        ),
        SearchableField(
            name="content",
            type=SearchFieldDataType.String,
            searchable=True,
        ),
        SimpleField(
            name="type",
            type=SearchFieldDataType.String,
            filterable=True,
        ),
        SimpleField(
            name="document_id",
            type=SearchFieldDataType.String,
            filterable=True,
        ),
        SimpleField(
            name="source",
            type=SearchFieldDataType.String,
            filterable=True,
        ),
        SearchableField(
            name="metadata",
            type=SearchFieldDataType.String,
            searchable=True,
        ),
    ]

    # Créer l'index
    index = SearchIndex(
        name=INDEX_NAME,
        fields=fields,
    )

    # Vérifier si l'index existe
    try:
        existing_index = index_client.get_index(INDEX_NAME)
        print(f"  ✅ Index existe déjà: {INDEX_NAME}")
    except:
        # Créer si n'existe pas
        index_client.create_index(index)
        print(f"  ✅ Index créé: {INDEX_NAME}")

    # Résumé
    print("\n" + "=" * 70)
    print("✅ SETUP RÉUSSI!")
    print("=" * 70)

    print(f"""
📊 Azure Search Service:
   Service: {SEARCH_SERVICE_NAME}
   Endpoint: {endpoint}
   Index: {INDEX_NAME}

🔑 Admin Key: {admin_key[:30]}...{admin_key[-10:]}

📝 Ajoute au .env:
   AZURE_SEARCH_ENDPOINT={endpoint}
   AZURE_SEARCH_ADMIN_KEY={admin_key}
   AZURE_SEARCH_INDEX_NAME={INDEX_NAME}

✅ Prêt pour l'implémentation du RAG!
""")

    # Sauvegarder
    credentials = {
        "endpoint": endpoint,
        "admin_key": admin_key,
        "index_name": INDEX_NAME,
        "service_name": SEARCH_SERVICE_NAME,
    }

    with open("azure_search_credentials.json", "w") as f:
        json.dump(credentials, f, indent=2)

    print("💾 Credentials sauvegardés dans: azure_search_credentials.json")

except Exception as e:
    print(f"\n❌ Erreur: {e}")
    print("\n💡 Assurez-vous que 'az login' a été exécuté")
    exit(1)
