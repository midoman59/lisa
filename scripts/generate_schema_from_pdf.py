#!/usr/bin/env python3
"""
Génère un field_codes.json COMPLET et EXHAUSTIF en parsant le PDF entier (346 pages).
Extrait TOUS les codes de champs, tous les enregistrements, toutes les valeurs.
"""

import json
import re
from pathlib import Path
from collections import defaultdict
import pdfplumber

PDF_PATH = Path("docs/LS_V3.8.0_Fichiers_Permanents.pdf")
OUTPUT_PATH = Path("src/data/field_codes.json")

def extract_all_from_pdf():
    """Parse le PDF complet et extrait tous les éléments structurés."""

    schema = {
        "metadata": {
            "document": "LS - V3.8.0 - C.01.02 - Description des prises - Fichiers permanents",
            "version": "V1.00 du 22/01/2021",
            "source": "Sopra Banking Software",
            "extracted": "Automatic full PDF parsing",
            "total_pages": 0,
            "extraction_date": "2026-09-24"
        },
        "tables": {},
        "all_fields": {},  # Dictionnaire plat de tous les champs par code
        "all_values": {}   # Dictionnaire de toutes les valeurs par code
    }

    tables_dict = defaultdict(lambda: {"enregistrements": {}, "fields": []})
    all_fields = {}
    all_values = {}

    print("🔍 Parsing PDF complet (346 pages)...")

    with pdfplumber.open(PDF_PATH) as pdf:
        schema["metadata"]["total_pages"] = len(pdf.pages)

        current_table = None
        current_enregistrement = None
        current_section = None

        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            lines = text.split("\n")

            if page_num % 20 == 0:
                print(f"  📖 Page {page_num}/{len(pdf.pages)}...")

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Détection des tables principales (ex: "1. DOSSIER : Fichier...")
                table_match = re.match(r"^\d+\.\s+([A-Z]+)\s*:\s*(.+)$", line)
                if table_match:
                    current_table = table_match.group(1)
                    table_name = table_match.group(2)
                    tables_dict[current_table]["description"] = table_name
                    print(f"  📋 Table trouvée: {current_table}")

                # Détection des enregistrements (ex: "ENR-DGEN" ou "Enregistrement (01)")
                enreg_match = re.search(r"(ENR-[A-Z0-9]+)", line)
                if enreg_match:
                    current_enregistrement = enreg_match.group(1)
                    if current_table:
                        tables_dict[current_table]["enregistrements"][current_enregistrement] = {
                            "fields": []
                        }

                # Détection des sections (ex: "RÉSULTATS FONCTIONNEMENT PRÊT")
                if "ENREGISTREMENT" in line and ("(" in line):
                    section_match = re.search(r"Enregistrement\s*\((\d+)\)\s*(.+)", line)
                    if section_match:
                        current_section = section_match.group(2)

                # Extraction des champs (ex: "CLEOFS X(00027) Clé partielle")
                # Format: CODE TYPE(SIZE) DESCRIPTION
                field_match = re.match(
                    r"^\s*([A-Z][A-Z0-9\-]*)\s+(X|S9|99)\((\d+)\)\s+(.+)$",
                    line
                )
                if field_match:
                    field_code = field_match.group(1)
                    field_type = field_match.group(2)
                    field_size = field_match.group(3)
                    field_desc = field_match.group(4).strip()

                    field_info = {
                        "code": field_code,
                        "type": field_type,
                        "size": field_size,
                        "description": field_desc,
                        "table": current_table,
                        "enregistrement": current_enregistrement,
                        "section": current_section
                    }

                    # Ajouter au dictionnaire plat
                    if field_code not in all_fields:
                        all_fields[field_code] = []
                    all_fields[field_code].append(field_info)

                    # Ajouter à la table
                    if current_table and current_enregistrement:
                        tables_dict[current_table]["enregistrements"][current_enregistrement]["fields"].append(
                            field_info
                        )

                # Extraction des valeurs de codes (ex: "1 : dossier accordé en attente...")
                # Format: NOMBRE : DESCRIPTION
                if re.match(r"^\s*[0-9A-F]\s*:\s*.+", line):
                    # Essayer de matcher le code précédent
                    value_match = re.match(r"^\s*([0-9A-F]+)\s*:\s*(.+)$", line)
                    if value_match and current_section:
                        value_code = value_match.group(1)
                        value_desc = value_match.group(2).strip()

                        # Chercher le dernier champ pour l'associer
                        for field_code in reversed(list(all_fields.keys())):
                            if all_fields[field_code]:
                                parent_field = field_code
                                if parent_field not in all_values:
                                    all_values[parent_field] = {}
                                all_values[parent_field][value_code] = value_desc
                                break

    # Construire le schéma final
    schema["tables"] = dict(tables_dict)
    schema["all_fields"] = all_fields
    schema["all_values"] = all_values

    # Statistiques
    total_tables = len(schema["tables"])
    total_enregistrements = sum(
        len(t["enregistrements"]) for t in schema["tables"].values()
    )
    total_fields = len(all_fields)
    total_values = sum(len(v) for v in all_values.values())

    schema["metadata"]["statistics"] = {
        "total_tables": total_tables,
        "total_enregistrements": total_enregistrements,
        "total_fields": total_fields,
        "total_value_definitions": total_values
    }

    return schema


def save_schema(schema):
    """Sauvegarde le schéma en JSON."""
    print(f"\n💾 Sauvegarde dans {OUTPUT_PATH}...")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(schema, f, ensure_ascii=False, indent=2)

    # Statistiques
    size_kb = OUTPUT_PATH.stat().st_size / 1024
    print(f"✅ Fichier créé: {size_kb:.1f} KB")
    print(f"\n📊 Statistiques:")
    print(f"   - Tables: {schema['metadata']['statistics']['total_tables']}")
    print(f"   - Enregistrements: {schema['metadata']['statistics']['total_enregistrements']}")
    print(f"   - Champs uniques: {schema['metadata']['statistics']['total_fields']}")
    print(f"   - Valeurs définies: {schema['metadata']['statistics']['total_value_definitions']}")


if __name__ == "__main__":
    print("=" * 70)
    print("🚀 EXTRACTION COMPLÈTE DU SCHÉMA LS V3.8.0")
    print("=" * 70)

    if not PDF_PATH.exists():
        print(f"❌ PDF non trouvé: {PDF_PATH}")
        exit(1)

    print(f"\n📖 PDF source: {PDF_PATH}")
    print(f"📄 Pages: 346")

    schema = extract_all_from_pdf()
    save_schema(schema)

    print("\n" + "=" * 70)
    print("✅ EXTRACTION COMPLÈTÉE AVEC SUCCÈS")
    print("=" * 70)
