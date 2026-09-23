#!/usr/bin/env python3
"""
Data Loader - Charge les données JSON locales
"""

import json
from pathlib import Path
from typing import List, Dict, Any

class DataLoader:
    """Charge et gère les données locales (Dossiers, Enregistrements, Événements)"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.dossiers: List[Dict[str, Any]] = []
        self.enregistrements: List[Dict[str, Any]] = []
        self.evenements: List[Dict[str, Any]] = []

        self.load_all()

    def load_all(self):
        """Charge tous les fichiers JSON"""
        self.dossiers = self._load_json("dossiers.json")
        self.enregistrements = self._load_json("enregistrements.json")
        self.evenements = self._load_json("evenements.json")

        print(f"✓ Loaded {len(self.dossiers)} dossiers")
        print(f"✓ Loaded {len(self.enregistrements)} enregistrements")
        print(f"✓ Loaded {len(self.evenements)} événements")

    def _load_json(self, filename: str) -> List[Dict[str, Any]]:
        """Charge un fichier JSON"""
        filepath = self.data_dir / filename
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  File not found: {filepath}")
            return []

    # ========== DOSSIERS ==========
    def get_dossiers(self) -> List[Dict[str, Any]]:
        """Retourne tous les dossiers"""
        return self.dossiers

    def get_dossier(self, numero: str) -> Dict[str, Any] | None:
        """Retourne un dossier par numéro"""
        for d in self.dossiers:
            if d.get("numero_dossier") == numero:
                return d
        return None

    def get_dossiers_by_statut(self, statut: str) -> List[Dict[str, Any]]:
        """Retourne les dossiers par statut"""
        return [d for d in self.dossiers if d.get("statut") == statut]

    def search_dossiers(self, query: str) -> List[Dict[str, Any]]:
        """Cherche les dossiers (par numéro ou client)"""
        query = query.lower()
        results = []
        for d in self.dossiers:
            if query in d.get("numero_dossier", "").lower() or \
               query in d.get("client_nom", "").lower():
                results.append(d)
        return results

    # ========== ENREGISTREMENTS ==========
    def get_enregistrements_by_dossier(self, dossier_id: str) -> List[Dict[str, Any]]:
        """Retourne les enregistrements d'un dossier"""
        return [e for e in self.enregistrements if e.get("dossier_id") == dossier_id]

    # ========== ÉVÉNEMENTS ==========
    def get_evenements_by_dossier(self, dossier_id: str) -> List[Dict[str, Any]]:
        """Retourne les événements d'un dossier"""
        return [evt for evt in self.evenements if evt.get("dossier_id") == dossier_id]

    def get_evenements_recents(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retourne les événements récents"""
        # Trier par date décroissante (plus récent d'abord)
        sorted_evt = sorted(
            self.evenements,
            key=lambda x: x.get("date_evenement", ""),
            reverse=True
        )
        return sorted_evt[:limit]

    # ========== ANALYSES ==========
    def get_dossier_summary(self, dossier_id: str) -> Dict[str, Any]:
        """Résumé complet d'un dossier avec DGEN, DPAY, DGAR"""
        dossier = next((d for d in self.dossiers if d.get("id") == dossier_id), None)
        if not dossier:
            return {}

        enreg = self.get_enregistrements_by_dossier(dossier_id)
        evt = self.get_evenements_by_dossier(dossier_id)

        # Extraire DGEN (données générales)
        dgen = dossier.get("dgen", {})

        # Extraire DPAY (payeurs) et DGAR (garanties) de tous les enregistrements
        dpays = [e.get("dpay") for e in enreg if e.get("dpay")]
        dgars = [e.get("dgar") for e in enreg if e.get("dgar")]

        return {
            **dossier,
            "nombre_enregistrements": len(enreg),
            "nombre_evenements": len(evt),
            "dgen": dgen,
            "enregistrements": enreg,
            "dpay_payeurs": dpays,
            "dgar_garanties": dgars,
            "evenements": evt
        }

    def get_statistics(self) -> Dict[str, Any]:
        """Statistiques générales (LS V3.8.0 - DGEN table)"""
        actifs = len(self.get_dossiers_by_statut("ACTIF"))
        fermes = len(self.get_dossiers_by_statut("FERMÉ"))

        # Utilise DGEN.montant_principal (table données générales)
        montant_total = sum(d.get("dgen", {}).get("montant_principal", 0) for d in self.dossiers)

        return {
            "total_dossiers": len(self.dossiers),
            "dossiers_actifs": actifs,
            "dossiers_fermes": fermes,
            "montant_total_accorde_eur": montant_total,
            "montant_moyen_eur": montant_total / len(self.dossiers) if self.dossiers else 0
        }


if __name__ == "__main__":
    # Test
    loader = DataLoader()

    print("\n=== STATISTIQUES ===")
    stats = loader.get_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")

    print("\n=== DOSSIERS ===")
    for d in loader.get_dossiers():
        print(f"  {d['numero_dossier']}: {d['client_nom']} ({d['statut']})")

    print("\n=== ÉVÉNEMENTS RÉCENTS ===")
    for evt in loader.get_evenements_recents(5):
        print(f"  {evt['date_evenement']}: {evt['type_evenement']} - {evt['montant_evenement']}€")
