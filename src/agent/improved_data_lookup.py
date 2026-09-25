#!/usr/bin/env python3
"""
Système de lookup amélioré pour les champs dpay/dgar et données structurées
Complément au RAG pour les requêtes sur les données métier
"""

import json
import re
from pathlib import Path
from typing import Optional, List, Dict, Any

class ImprovedDataLookup:
    """Lookup direct dans les données structurées (enregistrements, dossiers)"""

    # Mappage des keywords des requêtes utilisateur vers les champs des mocks
    FIELD_KEYWORDS = {
        # BIC/compte
        "bic": ["CDBIC-09", "dpay_code_bic"],
        "code bic": ["CDBIC-09", "dpay_code_bic"],
        "iban": ["dpay_reference_compte"],
        "compte": ["dpay_reference_compte", "dpay_type_compte"],
        "compte externe": ["dpay_type_compte"],
        "compte interne": ["dpay_type_compte"],
        "externe": ["dpay_type_compte"],
        "interne": ["dpay_type_compte"],

        # Garantie
        "garantie": ["dgar_type_garantie", "dgar_montant_garantie"],
        "type garantie": ["dgar_type_garantie"],
        "montant garantie": ["dgar_montant_garantie"],
        "hypotheque": ["dgar_type_garantie"],
        "hypo": ["dgar_type_garantie"],
        "nantissement": ["dgar_type_garantie"],
        "privilege": ["dgar_type_garantie"],

        # Paiement
        "paiement": ["dpay_montant_paiement", "dpay_mode_paiement"],
        "mode paiement": ["dpay_mode_paiement"],
        "montant paiement": ["dpay_montant_paiement"],
        "virement": ["dpay_mode_paiement"],
        "vir": ["dpay_mode_paiement"],
        "prelevement": ["dpay_mode_paiement"],
        "prlv": ["dpay_mode_paiement"],
    }

    def __init__(self):
        self.enregistrements = self._load_enregistrements()
        self.dossiers = self._load_dossiers()
        self.evenements = self._load_evenements()

    def _load_enregistrements(self) -> List[Dict]:
        """Charger les enregistrements"""
        try:
            path = Path(__file__).parent.parent.parent / "src" / "data" / "enregistrements.json"
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def _load_dossiers(self) -> List[Dict]:
        """Charger les dossiers"""
        try:
            path = Path(__file__).parent.parent.parent / "src" / "data" / "dossiers.json"
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def _load_evenements(self) -> List[Dict]:
        """Charger les événements"""
        try:
            path = Path(__file__).parent.parent.parent / "src" / "data" / "evenements.json"
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def detect_field_keywords(self, query: str) -> List[str]:
        """Détecte les keywords de champs dans la requête"""
        query_lower = query.lower()
        keywords = []

        for keyword in self.FIELD_KEYWORDS.keys():
            if keyword in query_lower:
                keywords.append(keyword)

        # Retourner les keywords les plus spécifiques (longer first)
        return sorted(keywords, key=len, reverse=True)

    def lookup_field_in_data(self, field_name: str) -> str:
        """Cherche une valeur de champ dans les données et retourne un contexte"""
        if not field_name:
            return ""

        lines = []

        # Chercher dans les enregistrements
        for enreg in self.enregistrements:
            if field_name in enreg:
                dos_id = enreg.get("dossier_id")
                dos = next((d for d in self.dossiers if d.get("id") == dos_id), None)
                dos_num = dos.get("numero_dossier") if dos else "?"

                value = enreg[field_name]
                lines.append(f"  {dos_id} ({dos_num}): {value}")

        if lines:
            return "\n".join(lines)
        return ""

    def search_by_keywords(self, query: str) -> Optional[str]:
        """Cherche les données basées sur les keywords de la requête"""
        keywords = self.detect_field_keywords(query)
        if not keywords:
            return None

        # Récupérer tous les champs associés aux keywords
        relevant_fields = set()
        for keyword in keywords:
            relevant_fields.update(self.FIELD_KEYWORDS.get(keyword, []))

        if not relevant_fields:
            return None

        # Chercher les valeurs de ces champs dans les données
        context_parts = []

        for field_name in sorted(relevant_fields):
            result = self.lookup_field_in_data(field_name)
            if result:
                context_parts.append(f"\n{field_name}:")
                context_parts.append(result)

        if context_parts:
            return "\n".join(context_parts)

        return None

    def format_context(self, query: str) -> str:
        """Formate le contexte trouvé directement dans les données"""
        result = self.search_by_keywords(query)

        if not result:
            return ""

        return (
            "\nDONNEES DIRECTES (lookup dans les enregistrements):\n"
            + "=" * 60 + "\n"
            + result + "\n"
        )
