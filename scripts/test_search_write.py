#!/usr/bin/env python3
"""
Test simple: Vérifier si on peut écrire dans Azure Search
"""

import os
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from azure.identity import AzureCliCredential, DefaultAzureCredential

load_dotenv()

ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME", "lisa-documents")

print("=" * 70)
print("🧪 TEST: Écriture dans Azure Search")
print("=" * 70)

print(f"\n📋 Configuration:")
print(f"   Endpoint: {ENDPOINT}")
print(f"   Index: {INDEX_NAME}")

# Test 1: Connexion
print(f"\n🔌 Test 1: Connexion...")
try:
    credential = AzureCliCredential()
    client = SearchClient(
        endpoint=ENDPOINT,
        index_name=INDEX_NAME,
        credential=credential
    )
    print("   ✅ Connexion OK")
except Exception as e:
    print(f"   ❌ Erreur connexion: {e}")
    exit(1)

# Test 2: Écriture simple
print(f"\n📝 Test 2: Écriture d'un document simple...")
try:
    test_doc = {
        "id": "test-doc-001",
        "content": "Ceci est un test de document",
        "type": "test",
        "document_id": "TEST001",
        "source": "test_script.py",
        "metadata": "test metadata"
    }

    print(f"   📤 Upload du document: {test_doc['id']}")
    client.upload_documents([test_doc])
    print("   ✅ Upload OK")

except Exception as e:
    print(f"   ❌ Erreur upload: {e}")
    print(f"\n💡 Erreur détaillée:")
    print(f"   Type: {type(e).__name__}")
    print(f"   Message: {str(e)}")
    exit(1)

# Test 3: Lecture
print(f"\n🔍 Test 3: Lecture du document...")
try:
    results = client.search(search_text="test")
    docs = list(results)
    print(f"   ✅ Lecture OK - Trouvé {len(docs)} document(s)")

    if docs:
        print(f"   Document trouvé: {docs[0]['id']}")
except Exception as e:
    print(f"   ❌ Erreur lecture: {e}")
    exit(1)

print("\n" + "=" * 70)
print("✅ TOUS LES TESTS PASSÉS!")
print("=" * 70)
print("\n💡 Si ça marche ici, le problème vient du script d'indexation")
print("   ou de la taille des documents.")
