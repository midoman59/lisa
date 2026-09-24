#!/usr/bin/env python3
"""
Version 2: Améliorée pour extraire AUSSI toutes les valeurs des codes.
"""

import json
import re
from pathlib import Path
from collections import defaultdict
import pdfplumber

PDF_PATH = Path("docs/LS_V3.8.0_Fichiers_Permanents.pdf")
OUTPUT_PATH = Path("src/data/field_codes.json")

def enhance_schema_with_values():
    """Lit le fichier JSON généré et enrichit avec les valeurs du PDF."""

    # Charger le schema existant
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)

    print("🔍 Enrichissement avec extraction des valeurs...")

    # Tracker les derniers champs vus pour les associer aux valeurs
    field_stack = []
    values_by_field = defaultdict(dict)
    current_section = None

    with pdfplumber.open(PDF_PATH) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            lines = text.split("\n")

            if page_num % 50 == 0:
                print(f"  📖 Page {page_num}/346...")

            for line in lines:
                original_line = line
                line = line.strip()
                if not line or len(line) < 3:
                    continue

                # Détecter les sections (ex: "code situation du dossier :")
                if ":" in line and not re.match(r"^\d+", line):
                    # Chercher un code de champ juste avant
                    field_match = re.search(r"([A-Z][A-Z0-9\-]*)\s+[A-Z]", original_line)
                    if field_match:
                        current_section = line

                # Extraire les valeurs possibles (ex: "1 : dossier accordé")
                value_match = re.match(r"^\s*([0-9A-Fa-f\-]+)\s*:\s*(.+)$", line)
                if value_match and len(line) > 5:
                    value_code = value_match.group(1).strip()
                    value_desc = value_match.group(2).strip()

                    # Trouver le dernier champ pertinent
                    if current_section:
                        # Chercher un champ associé à cette section
                        for table_info in schema["tables"].values():
                            for enreg_info in table_info.get("enregistrements", {}).values():
                                for field in enreg_info.get("fields", []):
                                    if current_section.lower() in field["description"].lower():
                                        field_code = field["code"]
                                        if field_code not in values_by_field:
                                            values_by_field[field_code] = {}
                                        values_by_field[field_code][value_code] = value_desc

    # Enrichir le schema avec les valeurs
    if values_by_field:
        schema["field_values"] = dict(values_by_field)
        total_vals = sum(len(v) for v in values_by_field.values())
        schema["metadata"]["statistics"]["total_value_definitions"] = total_vals
        print(f"  ✅ {total_vals} valeurs extraites")

    # Sauvegarder
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(schema, f, ensure_ascii=False, indent=2)

    print(f"✅ Fichier enrichi sauvegardé!")
    return schema

if __name__ == "__main__":
    print("=" * 70)
    print("🚀 ENRICHISSEMENT SCHEMA AVEC VALEURS")
    print("=" * 70)

    enhance_schema_with_values()

    print("\n" + "=" * 70)
    print("✅ ENRICHISSEMENT COMPLÉTÉ")
    print("=" * 70)
