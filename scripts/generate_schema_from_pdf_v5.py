#!/usr/bin/env python3
"""
V5: Extraction COMPLÈTE et ROBUSTE de tous les champs du PDF (346 pages).

Root cause du problème précédent: le script v1 (generate_schema_from_pdf.py)
n'a capturé que 27 champs uniques sur l'ensemble du document, car son regex
`^([A-Z][A-Z0-9\\-]*)\\s+(X|S9|99)\\((\\d+)\\)\\s+(.+)$` ne matchait que les
lignes où pdfplumber avait accidentellement isolé le nom du champ sur sa
propre ligne — la grande majorité des lignes de champs, qui suivent le format
tabulaire réel `* pos pos taille * niveau NOM TYPE(taille) [PACKE] * desc *`,
n'étaient jamais reconnues.

Ce script reconstruit "tables" et "all_fields" en parsant DIRECTEMENT ce
format tabulaire (avec gestion des lignes de continuation de description),
en suivant le fichier courant (DOSSIER/LIGNE/...) via l'en-tête de page pour
un scoping fiable.
"""

import json
import re
from pathlib import Path
from collections import defaultdict
import pdfplumber

PDF_PATH = Path("docs/LS_V3.8.0_Fichiers_Permanents.pdf")
OUTPUT_PATH = Path("src/data/field_codes.json")

HEADER_RE = re.compile(r"^Sopra Banking Software\s+\d{2}-\w{3}-\d{4}\s+([A-Z]+)\s+page\s+\d+\s*/\s*\d+")
ENREG_RE = re.compile(r"(ENR-[A-Z0-9]+)")

# * <start> <end> <size> * <level> <NAME> [occurs] TYPE(size)[V9(dec)] [PACKE] * description *
FIELD_ROW_RE = re.compile(
    r"^\*\s*\d+\s+\d+\s+\d+\s*\*\s*(\d+)\s+([A-Z][A-Z0-9\-]*)\s+(?:\d+\s+)?"
    r"(X\(\d+\)|S9\(\d+\)(?:V9\(\d+\))?|99)\s*(?:PACKE)?\s*\*\s*(.+?)\s*\*?\s*$"
)
# Continuation of a wrapped description: "* * * ...text... *"
CONTINUATION_RE = re.compile(r"^\*\s*\*\s*\*\s*(.+?)\s*\*?\s*$")
TABLE_INTRO_RE = re.compile(r"^\d+\.\s+([A-Z]+)\s*:\s*(.+)$")


def extract_all_fields():
    tables_dict = defaultdict(lambda: {"enregistrements": {}})
    all_fields = defaultdict(list)

    current_table = None
    current_enregistrement = None
    last_field_info = None  # for continuation-line description appending

    with pdfplumber.open(PDF_PATH) as pdf:
        total_pages = len(pdf.pages)
        print(f"🔍 Parsing complet ({total_pages} pages)...")

        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            lines = text.split("\n")

            if page_num % 50 == 0:
                print(f"  📖 Page {page_num}/{total_pages}...")

            for raw_line in lines:
                line = raw_line.strip()
                if not line:
                    continue

                header_match = HEADER_RE.match(line)
                if header_match:
                    current_table = header_match.group(1)
                    continue

                table_intro = TABLE_INTRO_RE.match(line)
                if table_intro:
                    current_table = table_intro.group(1)
                    continue

                enreg_match = ENREG_RE.search(line)
                if enreg_match:
                    current_enregistrement = enreg_match.group(1)
                    if current_table:
                        tables_dict[current_table]["enregistrements"].setdefault(
                            current_enregistrement, {"fields": []}
                        )
                    last_field_info = None
                    continue

                field_match = FIELD_ROW_RE.match(raw_line.strip())
                if field_match and current_table:
                    level, field_code, field_type, field_desc = field_match.groups()
                    field_info = {
                        "code": field_code,
                        "type": field_type,
                        "description": field_desc.strip(),
                        "table": current_table,
                        "enregistrement": current_enregistrement,
                        "level": level,
                    }
                    all_fields[field_code].append(field_info)
                    if current_table and current_enregistrement:
                        tables_dict[current_table]["enregistrements"].setdefault(
                            current_enregistrement, {"fields": []}
                        )
                        tables_dict[current_table]["enregistrements"][current_enregistrement]["fields"].append(
                            field_info
                        )
                    last_field_info = field_info
                    continue

                continuation_match = CONTINUATION_RE.match(raw_line.strip())
                if continuation_match and last_field_info:
                    extra = continuation_match.group(1).strip()
                    if extra:
                        last_field_info["description"] = (last_field_info["description"] + " " + extra).strip()
                    continue

                # Any other line breaks the continuation chain
                last_field_info = None

    return dict(tables_dict), dict(all_fields)


def save_schema(tables, all_fields):
    total_tables = len(tables)
    total_enregistrements = sum(len(t["enregistrements"]) for t in tables.values())
    total_fields = len(all_fields)
    total_occurrences = sum(len(v) for v in all_fields.values())

    schema = {
        "metadata": {
            "document": "LS - V3.8.0 - C.01.02 - Description des prises - Fichiers permanents",
            "version": "V1.00 du 22/01/2021",
            "source": "Sopra Banking Software",
            "extracted": "Automatic full PDF parsing (v5 - robust field-row regex)",
            "total_pages": 346,
            "extraction_date": "2026-09-24",
            "statistics": {
                "total_tables": total_tables,
                "total_enregistrements": total_enregistrements,
                "total_fields": total_fields,
                "total_field_occurrences": total_occurrences,
                "total_value_definitions": 0,
            },
        },
        "tables": tables,
        "all_fields": all_fields,
        "field_values": {},
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(schema, f, ensure_ascii=False, indent=2)

    size_kb = OUTPUT_PATH.stat().st_size / 1024
    print(f"\n✅ Fichier créé: {size_kb:.1f} KB")
    print(f"📊 Statistiques:")
    print(f"   - Tables: {total_tables}")
    print(f"   - Enregistrements: {total_enregistrements}")
    print(f"   - Champs uniques: {total_fields}")
    print(f"   - Occurrences totales de champs: {total_occurrences}")


if __name__ == "__main__":
    print("=" * 70)
    print("🚀 EXTRACTION V5: TOUS LES CHAMPS DU SCHÉMA LS V3.8.0")
    print("=" * 70)

    if not PDF_PATH.exists():
        print(f"❌ PDF non trouvé: {PDF_PATH}")
        exit(1)

    tables, all_fields = extract_all_fields()
    save_schema(tables, all_fields)

    print("\n" + "=" * 70)
    print("✅ EXTRACTION V5 COMPLÉTÉE")
    print("=" * 70)
