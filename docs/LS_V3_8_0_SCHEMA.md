# Schéma LS V3.8.0 - Fichiers Permanents
**Source**: LS - Loan Servicing - V3.8.0 - Intégration  
**Document**: C.01.02 - Description des prises - Fichiers permanents  
**Version**: 1.00 du 22/01/2021

---

## 1. DOSSIER - Fichier des dossiers de prêt

### Structure Principale (ENR-DOSSIER)
```
Clé: CLEDOG (Clé partielle du fichier DOSSIER)
Zone de groupe: IDERENEG (Identifiant enregistrement), NOENR-D (Numéro d'enregistrement)

Enregistrement (01) - Données de lancement:
- CLEDOG: Clé partielle (X'00027')
- IDERENEG: Identifiant enregistrement (X'00005')
- NOENR-D: Numéro d'enregistrement (9'00002')
- DIFL001: Date de création du fichier (zone de groupe)
- DFIC: Date de création du fichier (89'00009')
- DTDGMCIV: Date de dernière traitement fin de mois (89'00009')
- DED: Date de dernière traitement déclarations (89'00009')
- NOVERSION: Numéro de version de Loan Engine (X'00008')
```

### Enregistrement (02) - Données de lancement (Compiègne):
```
- CLEDOG8: Clé du fichier (X'00034')
- IDERENEG8: Identifiant enregistrement (X'00005')
- Zone de groupe: FS-12, F2-12 (X'00005')
- REPAIS-12 (X'00012')
- INDICATEURS DE SAISIE (nombreux flags)
- CDDEVI8E-12 (X'00001')
- INDICATEURS DOSSIER (multiples champs)
- INDREL-12 (X'00001')
- INLANCB-12 (X'00001')
- INCJS-12 (X'00001')
```

---

## 2. DGEN - Données Générales (Enregistrement Clés pour DOSSIER)

### Structure DGEN (Enregistrement 03):
```
ASSIGNOG-DGEN (Données générales):
  - CLEDOG: Clé partielle (X'00027')
  - IDERENEG: Identifiant enregistrement (X'00005')
  - FS-13: Zone de groupe (X'00005')
  - F2-13: (X'00002')
  - REPAIS-13 (X'00012')
  - INDICATEURS DE SAISIE:
    - VERISPO-13: Vérification ISO pays (voir ci-après)
    - MGTSOBAL-13: Montant global de risque
    - INANCOBS-13: Indicateurs d'ancien dossier
    - CFFENCOS-13: Catégorie financement
    - CDSIOP-13: Code siège de la place
    - TYPRELE-13: Type de prêt
    - INDIODE-13: Indicateur de dossier réel
    - CUDASICE-13: Code devise
    - ELUSOC-13: Code de la société
    - MERISQ-13: Montant global de risque
    - MGTSOBAL-13: Montant global du syndical
    - INANCOBS-13: Indicateurs d'ancien dossier
    - CFFENCOS-13: Catégorie financement
    - CDSIOP-13: Code siège de la place
    - TYPRELE-13: Type de prêt
    - Etc...
```

---

## 3. LIGNE - Fichier des dossiers de ligne (Enregistrements)

### Enregistrement Principal (01):
```
ASSIGNOG-LIGNE:
  - CLEDOG: Clé partielle (X'00027')
  - IDERENEG: Identifiant enregistrement (X'00005')
  - NOENR-L: Numéro d'enregistrement (9'00002')
  - Zone de groupe: DIFLANCE (X'00037')
  - DFIC: Date de création (89'00009')
  - REPAIS-L: Référence du prêt
  - CDEVI: Code devise
  - MONNORMA-L: Montant normalisé de la ligne
  - DUREE-L: Durée du dossier
  - DTREALISA-L: Date de réalisation
  - DPROCHE-ECHEA-L: Date de prochaine échéance
  - DPROCHA-TRAITPERIOD-L: Date de prochain traitement périodique
  - DTDGMCIV: Date de dernière traitement fin de mois
  - TYPRELE-L: Type de prêt
  - Etc...
```

---

## 4. EVTDOS - Fichier des événements dossier

### Structure (01) Enregistrement de début:
```
ASSIGNOD-EVTDOS:
  - CLEREVTDOS: Clé du fichier EVTDOS (X'00051')
  - IDENTDOG: Zone de groupe
  - DTVVALEUR: Date de valeur de l'événement
  - NOEORDRE: Numéro d'ordre
  - DVALEREVT: Date de valeur de l'événement
  - NOEORDRE: Numéro d'ordre
  - DEVTENBRO: Numéro d'ordre
  - DEFILTRAIT: Zone de groupe du fichier
  - DFTC: Date de création
  - DTDGMCIV: Date de dernière traitement fin de mois
  - DTDGMCCB: Date de dernière traitement déclarations
  - NOVERSION: Numéro de version de Loan Engine (X'00008')
```

---

## 5. Tables Secondaires (Dépendantes de DOSSIER et LIGNE)

### ECHIMP - Fichier des échéances impayées
- Lié à LIGNE
- Contient informations sur paiements en retard

### REVOLVING - Fichier des dossiers revolving
- Variante de LIGNE pour crédits revolving
- Structure similaire mais adaptée au type de crédit

### ECHANT - Fichier des échéances à anticiper
- Événements futurs planifiés

### HISTDOS - Historique des dossiers
- Archive historique de DOSSIER

### HISTDOSV - Historique des dossiers (variante)
- Archive historique avec détails supplémentaires

---

## 6. Correspondances entre Tables

```
DOSSIER (principale)
  ├── DGEN (Données générales du dossier)
  ├── LIGNE (Enregistrements/Lignes du dossier)
  │   ├── ECHIMP (Échéances impayées)
  │   ├── REVOLVING (Si crédit revolving)
  │   └── ECHANT (Échéances anticipées)
  ├── EVTDOS (Événements du dossier)
  ├── HISTDOS (Historique)
  └── HISTDOSV (Historique variant)
```

---

## 7. Recommandations pour Agent Data

**Pour votre démo avec agent**, incluez:

1. **Table DGEN** - Données de base du dossier (statut, montants, client)
2. **Table LIGNE** - Enregistrements/tranches du dossier
3. **Table EVTDOS** - Événements (paiements, clôtures, modifications)
4. **Table ECHIMP** - Échéances impayées (si applicable)

Ces 4 tables suffisent pour une démo complète du système.

---

## 8. Attributs Clés pour les Requêtes Agent

### DGEN - Attributs essentiels:
- CLEDOG: Identifiant dossier
- MGTSOBAL: Montant global
- CUDASICE: Devise
- TYPRELE: Type de prêt
- Statut du dossier
- Client/Emprunteur

### LIGNE - Attributs essentiels:
- CLEDOG: Ref. dossier parent
- NOENR-L: Numéro ligne
- MONNORMA-L: Montant de la ligne
- DUREE-L: Durée
- DFIC: Date création
- TYPRELE-L: Type

### EVTDOS - Attributs essentiels:
- CLEREVTDOS: Identifiant événement
- DTVVALEUR: Date événement
- NOEORDRE: Numéro ordre
- Type d'événement
- Montant si applicable

---

## Références

**Document source**: 
- LS - V3.8.0 - C.01.02 - Intégration - Description des prises - Fichiers permanents_V1.00.pdf

**Pages**: 
- DOSSIER: 1-49
- LIGNE: 53-111
- REVOLVING: 112-137
- ECHIMP: 138-147
- EVTDOS: 149-157
