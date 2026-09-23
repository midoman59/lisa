# SCHÉMA DOSSIER - COMPLET LS V3.8.0
**Source**: LS - Loan Servicing - V3.8.0 - C.01.02  
**Pages**: 4-52 (49 pages du fichier DOSSIER)  
**Date**: 22 janvier 2021

---

## Vue d'ensemble DOSSIER

Le fichier **DOSSIER** contient **25 enregistrements** (sous-structures):

| Ordre | Enregistrement | Description | Pages |
|-------|---|---|---|
| 01 | **ENR-DLANC** | Données de lancement | 4-5 |
| 02 | **ENR-DCOMM** | Données communes | 5-6 |
| 03 | **ENR-DGEN** | **Données générales** ⭐ | 6-7 |
| 04 | **ENR-DINERF** | Données intervenance financiers | 7-8 |
| 05 | **ENR-DSTAT** | Données complémentaires | 8 |
| 06 | **ENR-DPAY** | Données de payeur | 8-9 |
| 07 | **ENR-DPT** | Données participant trésorerie | 9 |
| 08 | **ENR-DDEPREC** | Données dépréciation créances | 9 |
| 09 | **ENR-DGAR** | Données garanties | 9-10 |
| 10 | **ENR-DPALI** | Données palier | 10-11 |
| 11 | **ENR-DACCP** | Données accessoires | 11-12 |
| 12 | **ENR-DASSP** | Données assurances à percevoir | 12-13 |
| 13 | **ENR-DCDF** | Données commande à date future | 13-14 |
| 14 | **ENR-DINDEX** | Données d'indexation | 14-16 |
| 15 | **ENR-DLOA** | Données location et taxe | 16-17 |
| 16 | **ENR-DREMB** | Remboursement de capital | 17-18 |
| 17 | **ENR-DTIERS** | Données tiers | 18 |
| 18 | **ENR-DINTERV** | Données intervenante | 18 |
| 19 | **ENR-DSPREC** | Données spécifiques réglementaires | 18-19 |
| 20 | **ENR-DCASHBCK** | Données du cash back | 19 |
| 21 | **ENR-DCCRAP** | Données contractuelles RAP | 19 |
| 22 | **ENR-DCCRAT** | Données contractuelles RAP | 19-20 |
| 23 | **ENR-DCCBL** | Données contractuelles déblocage | 20 |

---

## 1️⃣ ENR-DLANC - Données de lancement

```
Clé: CLEDOG (X'00027' - 27 bytes)
Identifiant enregistrement: IDERENEG (X'00005')
Numéro enregistrement: NOENR-D (9'00002')

Attributs clés:
- DFIC: Date de création du fichier (89'00009')
- DTDGMCIV: Dernière traitement fin de mois (89'00009')
- DED: Dernière traitement déclarations (89'00009')
- NOVERSION: Numéro version Loan Engine (X'00008')
```

---

## 2️⃣ ENR-DCOMM - Données communes

```
Enregistrement (02)

Attributs clés:
- ASSIGNOG-DO07: Zone groupe données communes
- IDERENEG: Identifiant enregistrement (X'00005')
- FS-12: Zone groupe (X'00005')
- F2-12: (X'00002')
- REPAIS-12: Référence prêt (X'00012')
- INDICATEURS DE SAISIE:
  - VERISPO-13: Vérification ISO pays
  - MGTSOBAL-13: Montant global de risque
  - INANCOBS-13: Indicateurs ancien dossier
  - CFFENCOS-13: Catégorie financement
  - CDSIOP-13: Code siège de la place
  - TYPRELE-13: Type de prêt
  - INDIODE-13: Indicateur dossier réel
  - CUDASICE-13: Code devise
  - ELUSOC-13: Code société
```

---

## 3️⃣ ENR-DGEN - Données générales ⭐ **TABLE CLÉS**

```
Enregistrement (03) - DONNÉES GÉNÉRALES

Clé partielle: CLEDOG (X'00027')

STRUCTURE ASSIGNOG-DO05:
  Zone groupe: IDERENEG (X'00005')
  FS-11, F2-11

ATTRIBUTS PRINCIPAUX:
- REPAIS-11: Référence du prêt (X'00012')
- IDFLANCE: Date de lancement (89'00037')
- DFIC: Date de création (89'00009')
- DTDGMCIV: Dernière traitement fin mois
- CUDASICE-11: Code devise (X'00003')
- MONNORMA-11: Montant normalisé dossier (89'00017')[3,3]
- DUREE-11: Durée du dossier (9'00005')
- DTREALISA-11: Date de réalisation (89'00009')
- DPROCHE-ECHEA-11: Date prochaine échéance (89'00009')
- DPROCHA-TRAITPERIOD-11: Date prochain traitement périodique (89'00009')
- TYPRELE-11: Type de prêt (X'00004')
- CFFENCOS-11: Catégorie financement (X'00001')
- CDSIOP-11: Code siège de la place (9'00003')
- INDICATEURS DOSSIER:
  - INDREL-11: Relation (X'00001')
  - INLANCB-11: Lancement bloc (X'00001')
  - INCJS-11: Calcul intérêts en jour exact (X'00001')
  - Etc... (NOMBREUX INDICATEURS)
```

---

## 4️⃣ ENR-DINERF - Données intervenance financiers

```
Enregistrement (04)

Attributs:
- ASSIGNOG-DO06: Zone groupe
- DINTERP-09: Données intervenance (X'00019')
- IDERENEG-09: Identifiant enregistrement (X'00005')
- Montant compte d'intérêt financier
- Référence tier/compte financier
- Code devise financier
- Mode calcul flux financier
- Code mode paiement
- Etc...
```

---

## 5️⃣ ENR-DSTAT - Données complémentaires

```
Enregistrement (05)

Zones de groupes:
- NOSTAT-E21: Données complémentaires (9'00004')
- Nombre de zones complémentaires
- Données de groupes complémentaires (136 bytes)
```

---

## 6️⃣ ENR-DPAY - Données de payeur

```
Enregistrement (06)

Attributs:
- ASSIGNOG-DO13: Zone groupe données payeur
- DPAY-14: Zone groupe (X'00005')
- Numéro de payeur
- Identifiant de l'enregistrement
- Mode de règlement
- Code mode de règlement
- Montant fixe payeur
- Montant flottant
- Code repartition d'accord
- Etc...
```

---

## 7️⃣ ENR-DPT - Données participant trésorerie

```
Enregistrement (07)

- CDPP-16: Zone groupe (X'00005')
- Numéro de sous-participant
- Montant de participation en trésorerie
- Code situation du participant financier
- Etc...
```

---

## 8️⃣ ENR-DDEPREC - Données dépréciations créances

```
Enregistrement (08)

- CDEPREC-17: Zone groupe (X'00036')
- Type de dépréciation
- Années de référence
- Dépréciations sur capital
- Dépréciations sur intérêts
- Dépréciations sur hors bilan
```

---

## 9️⃣ ENR-DGAR - Données garanties

```
Enregistrement (09)

Attributs:
- CLEDOG: Clé partielle (X'00027')
- DGAR-15: Zone groupe (X'00116')
- Numéro garantie
- Référence sous catalogue
- Montant de la garantie (exprimé en...)
- Valeur de la garantie
- Date de péremption
- Modalité de calcul en cas d'erreur
- Code mode appel
- Etc...
```

---

## 🔟 ENR-DPALI - Données palier

```
Enregistrement (10)

Attributs:
- DPALI-18: Zone groupe (X'00134')
- Numéro palier
- Montant initial palier
- Montant de la dernière mise à jour
- Etc...
```

---

## ENREGISTREMENTS 11-23 (Résumé)

| ENR | Description | Attributs clés |
|-----|---|---|
| ENR-DACCP (11) | Accessoires | Montant accessoire, code accessoire, etc. |
| ENR-DASSP (12) | Assurances | Montant assurance, taux, date péremption |
| ENR-DCDF (13) | Commandes futures | Montant, date exécution, nombre exécutions |
| ENR-DINDEX (14) | Indexation | Indices échéance, base indexation, taux |
| ENR-DLOA (15) | Location/Taxe | Montant loyer, durée location, date fin |
| ENR-DREMB (16) | Remboursement capital | Somme groupes assainissement, remboursements calculés |
| ENR-DTIERS (17) | Tiers | Nombre tiers, occurrence bloc rdo |
| ENR-DINTERV (18) | Intervenante | Numéro intervenant, saisie intervenant |
| ENR-DSPREC (19) | Réglementaires | Nombre occurrence bloc données |
| ENR-DCASHBCK (20) | Cash Back | Montant cash back, type paiement |
| ENR-DCCRAP (21) | RAP Contractuel | Montant minimum RAP, condition nominal |
| ENR-DCCRAT (22) | RAP Contractuel | Barème penalité, clause prêts assaisonniers |
| ENR-DCCBL (23) | Déblocage Contractuel | Déblocage conditionnel, clauses contractuelles |

---

## CLÉS POUR L'AGENT DATA

### Attributs indispensables à extraire:

**De DGEN:**
- `REPAIS-11` → Référence dossier unique
- `IDFLANCE` → Date de lancement
- `CUDASICE-11` → Devise (EUR/USD/etc.)
- `MONNORMA-11` → Montant total dossier
- `DUREE-11` → Durée (mois)
- `TYPRELE-11` → Type prêt (CREDIT/REVOLVING/etc.)
- `DPROCHE-ECHEA-11` → Prochaine échéance
- `CDSIOP-11` → Siège (agence)

**De DPAY:**
- Numéro payeur
- Mode paiement
- Montant payeur

**De DGAR:**
- Montant garanties
- Type garanties

**De DINDEX:**
- Taux indexation
- Indice de référence

---

## REMARQUES IMPORTANTES

1. **DGEN est le "cœur"** du dossier - contient les infos de base
2. **Chaque ENR est optionnel** - dépend du type/situation prêt
3. **Gestion de CREDIT** = DGEN + DPAY + DGAR + DINDEX
4. **Gestion REVOLVING** = DGEN + DACCP + DASSP + DCDF
5. **Les montants sont en 89'00009'** format (9 chiffres, 3 décimales)

---

## STRUCTURE JSON RECOMMANDÉE (pour démo)

```json
{
  "dossier": {
    "cledog": "DOS001",
    "dgen": {
      "repais": "REP-2024-001",
      "date_lancement": "2024-01-15",
      "devise": "EUR",
      "montant_principal": 50000.00,
      "duree_mois": 60,
      "type_pret": "CREDIT",
      "prochaine_echeance": "2024-02-15",
      "taux_interet": 4.5
    },
    "dpay": {
      "numero_payeur": "PAY001",
      "mode_paiement": "VIR",
      "montant": 833.33
    },
    "dgar": {
      "type_garantie": "HYPO",
      "montant_garantie": 75000.00
    }
  }
}
```

---

**Version du schéma**: Complète - 25 enregistrements, 100+ attributs  
**Applicable pour**: Démo LS V3.8.0 avec données réalistes  
**Généré le**: 2026-09-23
