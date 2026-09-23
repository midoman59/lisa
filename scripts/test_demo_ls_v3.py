#!/usr/bin/env python3
"""
Test Démo - Affiche les données LS V3.8.0 (DGEN, DPAY, DGAR)
"""

import json
from data_loader import DataLoader

def print_section(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def main():
    loader = DataLoader()

    # === STATISTIQUES ===
    print_section("STATISTIQUES GLOBALES")
    stats = loader.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # === DOSSIERS AVEC DGEN ===
    print_section("DOSSIERS (avec table DGEN - Données Générales)")
    for d in loader.get_dossiers():
        print(f"\n  📋 Dossier: {d['numero_dossier']}")
        print(f"     Client: {d['client_nom']}")
        print(f"     Statut: {d['statut']}")

        dgen = d.get("dgen", {})
        if dgen:
            print(f"\n     ▶ TABLE DGEN (Données Générales):")
            print(f"        - Référence: {dgen.get('repais')}")
            print(f"        - Date lancement: {dgen.get('date_lancement')}")
            print(f"        - Montant principal: {dgen.get('montant_principal')}€")
            print(f"        - Devise: {dgen.get('devise')}")
            print(f"        - Type prêt: {dgen.get('type_pret')}")
            print(f"        - Durée: {dgen.get('duree_mois')} mois")
            print(f"        - Taux: {dgen.get('taux_interet_base')}%")
            print(f"        - Prochaine échéance: {dgen.get('prochaine_echeance')}")
            print(f"        - Catégorie: {dgen.get('categorie_financement')}")

    # === ENREGISTREMENTS AVEC DPAY ET DGAR ===
    print_section("ENREGISTREMENTS (avec tables DPAY & DGAR)")
    for enreg in loader.enregistrements:
        print(f"\n  📝 Enregistrement: {enreg['id']}")
        print(f"     Type: {enreg['type_enregistrement']}")
        print(f"     Montant: {enreg['montant_initial']}€")
        print(f"     Taux: {enreg['taux_interet']}%")

        # DPAY - Données de payeur
        dpay = enreg.get("dpay", {})
        if dpay:
            print(f"\n     ▶ TABLE DPAY (Données Payeur):")
            print(f"        - Numéro payeur: {dpay.get('numero_payeur')}")
            print(f"        - Mode paiement: {dpay.get('mode_paiement')}")
            print(f"        - Montant paiement: {dpay.get('montant_paiement')}€")
            print(f"        - Dernier paiement: {dpay.get('date_dernier_paiement')}")
            print(f"        - IBAN: {dpay.get('reference_compte')}")

        # DGAR - Données de garanties
        dgar = enreg.get("dgar", {})
        if dgar:
            print(f"\n     ▶ TABLE DGAR (Données Garanties):")
            print(f"        - Numéro garantie: {dgar.get('numero_garantie')}")
            print(f"        - Type: {dgar.get('type_garantie')}")
            print(f"        - Montant garanti: {dgar.get('montant_garantie')}€")
            print(f"        - Couverture: {dgar.get('pourcentage_couverture')}%")
            print(f"        - Date prise d'effet: {dgar.get('date_prise_effet')}")
            print(f"        - Statut: {dgar.get('statut_garantie')}")

    # === RÉSUMÉ DOSSIER DÉTAILLÉ ===
    print_section("RÉSUMÉ DÉTAILLÉ - Dossier LS-2024-001")
    dos001 = loader.get_dossiers()[0]
    summary = loader.get_dossier_summary(dos001["id"])

    print(f"\n  📊 Données Générales (DGEN):")
    dgen_summary = summary.get("dgen", {})
    print(f"     {json.dumps(dgen_summary, indent=6, ensure_ascii=False)}")

    print(f"\n  💳 Payeurs (DPAY):")
    dpays = summary.get("dpay_payeurs", [])
    for dpay in dpays:
        print(f"     {json.dumps(dpay, indent=6, ensure_ascii=False)}")

    print(f"\n  🔐 Garanties (DGAR):")
    dgars = summary.get("dgar_garanties", [])
    for dgar in dgars:
        print(f"     {json.dumps(dgar, indent=6, ensure_ascii=False)}")

    # === ÉVÉNEMENTS ===
    print_section("ÉVÉNEMENTS RÉCENTS")
    for evt in loader.get_evenements_recents(6):
        print(f"\n  📅 {evt['date_evenement']} - {evt['type_evenement']}")
        print(f"     Montant: {evt['montant_evenement']}€")
        print(f"     Description: {evt['description']}")

    print_section("✅ DÉMO TERMINÉE - Schéma LS V3.8.0")
    print("Tables chargées: DGEN (Données Générales) + DPAY (Payeurs) + DGAR (Garanties)")
    print("= " * 70)

if __name__ == "__main__":
    main()
