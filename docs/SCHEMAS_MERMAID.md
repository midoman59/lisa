# LS V3.8.0 - Schémas Exacts de Base de Données

Basé sur **LS - V3.8.0 - C.01.02 - Description des prises - Fichiers permanents** (346 pages)

**STRUCTURE DÉTAILLÉE AVEC VRAIS CODES DE CHAMPS ET VALEURS**

## Sommaire des Tables Principales

| Numéro | Table | Code | Description | Pages |
|--------|-------|------|-------------|----- |
| 1 | DOSSIER | ENR-DGEN | Fichier des dossiers de prêt | 4-49 |
| 2 | LIGNE | ENR-DLIGN | Fichier des dossiers de ligne | 53-111 |
| 3 | REVOLVING | ENR-DREV | Fichier des dossiers revolving | 112-137 |
| 4 | ECHIMP | ENR-ECHIMP | Fichier des échéances impayées | 138-148 |
| 5 | EVTDOS | ENR-EVTDOS | Fichier des événements dossier | 149-157 |

---

## 1. Table DOSSIER (DGEN) - Fichier des dossiers de prêt

**Pages: 4-49 | Code: ENR-DGEN**

### Structure: Enregistrements et Zones

DGEN contient 7 enregistrements différents (01-02-38-39-43-44-62) avec zones de données.

### ENREGISTREMENT (01): DONNÉES DE LANCEMENT

**Code Champs Clés:**

| Code | Type | Taille | Description | Valeurs/Exemples |
|------|------|--------|-------------|-------------------|
| CLEOFS | X(27) | 27 | Clé partielle = identifie le dossier | DEI|FRANCE|DOSSIER-001 |
| IDDOSRG | X(5) | 5 | Identifiant de l'enregistrement | O1 (Enregistrement 01) |
| NOENREG | 99(9) | 9 | Numéro d'occurrence du bloc |  |
| NOENREG | 99 | Numéro de jour dans le mois | JJ de la zone DTECH-12 |
| ABRNNAT | 99 | Numéro d'occurrence des zones résultats accessoire à percevoir | groupées par nature |

---

### ENREGISTREMENT (50): RÉSULTATS - CODES STATUS DOSSIER

**Pages: 46 | CRITIQUES POUR LE RAG**

#### CDSITC-22: Code situation comptable du dossier
```
blanc = prêt en situation normale
3 = prêt douteux (si déclaissement manuel)
4 = prêt compromis (si déclaissement manuel)
5 = prêt compromis (si déclaissement automatique)
```
**Classe prêt (Table P039 poste 4-6):** codes prédéfinis pour différents niveaux de risque

#### CDSITDOS-22: Code situation du dossier *** CRITICAL ***
```
1 = dossier accordé en attente de réalisation
2 = dossier en cours d'amortissement
3 = dossier en attente de prise en charge données financières (RAP, blocage)
4 = dossier en attente de reprise
5 = dossier soldé ← C'EST LA VALEUR POUR "DOSSIER SOLDÉ" (NOT 6)
```
**Valeurs possibles:** 1, 2, 3, 4, 5 uniquement (5 valeurs totales)

#### CDMOTIF-22: Code motif solde du dossier
```
0 = dossier solde à blanc
1 = après RAT (crédit amortissable classique)
2 = après passage en contentieux
3 = après passage en continu
et autres codes spécifiques au type de clôture
```

#### INDAMOR-22: Indicateur d'amortissement
```
0 = au départ, on pour un dossier de type 0
1 = à partir de l'échéance où commence la phase de prorogatione, avant le dernier débloc
3 = à partir de l'anticipation de l'échéance ou commence la phase de prorogatione jusqu'à
4 = à partir de la commande de dernier débloc, sans réduction de nominal
5 = à partir de fin d'utilisation attente
6 = après reprise après modif données financières
7 = reprise après modif données financières
8 = blocage
9 = modification date prochaine échéance d'engagement
A = déblocage progressif
B = modification date début du contrat à date future
D = passage à taux indexé, changement d'index
E = report d'échéance
F = passage à taux fixe
```

---

## 2. Table LIGNE (DPAY) - Fichier des dossiers de ligne

**Pages: 53-111 | Code: ENR-DLIGN**

Chaque ligne de crédit associée à un dossier principal. Plusieurs lignes par CLEOFS.

### Champs Clés

### Diagramme DOSSIER

```mermaid
graph TD
    A["📋 DOSSIER<br/>Enregistrement DGEN"] -->|Base| B["Identifiants"]
    A -->|Contrats| C["Contrat & Client"]
    A -->|Financements| D["Montants & Taux"]
    A -->|Dates| E["Chronologie"]
    A -->|États| F["Statut & Codes"]
    A -->|Indicateurs| G["Flags & Signaux"]
    
    B -->|Détail| B1["CLEOFS: Clé partielle<br/>IDDOSRG: Enregistrement<br/>NOENREG: Bloc N°"]
    C -->|Détail| C1["Numéro dossier<br/>Client ID<br/>Ref société"]
    D -->|Détail| D1["Montant demandé<br/>Montant approuvé<br/>Taux intérêt<br/>Durée (mois)"]
    E -->|Détail| E1["Date ouverture<br/>Date fermeture<br/>Date signature<br/>Dernière modification"]
    F -->|Détail| F1["Statut dossier<br/>Code produit<br/>Zone groupe"]
    G -->|Détail| G1["Indicateur saisie<br/>Indicateur édition<br/>Flagsstatutaires"]
    
    style A fill:#4CAF50,color:#fff
    style B fill:#2196F3,color:#fff
```

### Exemples de Champs DOSSIER

```
Enregistrement (01) données de lancement:
• CLEOFS (Clé partielle): identifie le dossier de crédit
• IDDOSRG (Enregistrement O1): données de lancement de trésorier
• Indicateur saisie (voir ci-après)
• Zone de groupe : (Commande à date future ou répétitive)
• Date de création du dossier
• Date de dernière traitement périodique
• Date de dernière traitement mensuel ou fin de mois
• Date de dernières déclarations mensuelles
• Numéro d'enregistrement annuel
```

---

## 2. Table LIGNE (DPAY) - Fichier des dossiers de ligne

**Pages: 53-111 | Code: ENR-DLIGN**

Chaque ligne de crédit associée à un dossier principal.

```mermaid
graph TD
    A["💳 LIGNE<br/>Enregistrement DLIGN"] -->|Référence| B["Clés & Relations"]
    A -->|Financement| C["Montants & Taux"]
    A -->|Dates| D["Dates Clés"]
    A -->|Garanties| E["Provisions & Couverture"]
    A -->|Paiements| F["Remboursements"]
    
    B -->|Détail| B1["Clé ligne<br/>CLEOFS: Dossier parent<br/>Numéro ligne"]
    C -->|Détail| C1["Montant nominal<br/>Montant utilisé<br/>Montant restant<br/>Taux d'intérêt"]
    D -->|Détail| D1["Date mise en place<br/>Date première perception<br/>Date dernière perception"]
    E -->|Détail| E1["Indicateurs garantie<br/>Indicateurs risque<br/>Codes préemption"]
    F -->|Détail| F1["Montant paiement<br/>Intérêts payés<br/>Commissions<br/>Pénalités"]
    
    style A fill:#2196F3,color:#fff
```

---

## 3. Table REVOLVING (DREV) - Fichier des dossiers revolving

**Pages: 112-137 | Code: ENR-DREV**

Pour lignes de crédit revolving (utilisable sans nouvelle demande).

```mermaid
graph TD
    A["🔄 REVOLVING<br/>Enregistrement DREV"] -->|Limites| B["Plafonds"]
    A -->|Utilisation| C["Draws & Utilisations"]
    A -->|Dates| D["Dates Revolving"]
    
    B -->|Détail| B1["Plafond initial<br/>Plafond actuel<br/>Plafond autorisé"]
    C -->|Détail| C1["Montant utilisé<br/>Disponible<br/>Tirage courant"]
    D -->|Détail| D1["Depuis: Date<br/>Prochain réajustement<br/>Révision"]
    
    style A fill:#FF9800,color:#fff
```

---

## 4. Table ECHIMP - Échéances Impayées

**Pages: 138-148 | Code: ENR-ECHIMP**

Historique des échéances non payées et retards.

```mermaid
graph TD
    A["⚠️ ECHIMP<br/>Échéances Impayées"] -->|Identification| B["Références"]
    A -->|Montants| C["Sommes dues"]
    A -->|Dates| D["Chronologie"]
    
    B -->|Détail| B1["Clé dossier<br/>Clé ligne<br/>Numéro échéance"]
    C -->|Détail| C1["Montant principal<br/>Intérêts<br/>Pénalités"]
    D -->|Détail| D1["Date échéance prévue<br/>Date constatation retard<br/>Date dernière action"]
    
    style A fill:#F44336,color:#fff
```

---

## 5. Table EVTDOS - Événements Dossier

**Pages: 149-157 | Code: ENR-EVTDOS**

Journal des événements : modifications, actions, décisions.

```mermaid
graph TD
    A["📌 EVTDOS<br/>Événements Dossier"] -->|Référence| B["Identifiant"]
    A -->|Événement| C["Nature & Type"]
    A -->|Dates| D["Quand"]
    A -->|Responsable| E["Qui & Où"]
    
    B -->|Détail| B1["Clé dossier<br/>Numéro événement<br/>Code événement"]
    C -->|Détail| C1["Type d'événement<br/>Code action<br/>Description"]
    D -->|Détail| D1["Date événement<br/>Heure<br/>Timestamp"]
    E -->|Détail| E1["Utilisateur<br/>Agence<br/>Terminal"]
    
    style A fill:#9C27B0,color:#fff
```

---

## Schéma Relationnel Complet

```mermaid
erDiagram
    DOSSIER ||--o{ LIGNE : contient
    DOSSIER ||--o{ REVOLVING : utilise
    LIGNE ||--o{ ECHIMP : genere
    DOSSIER ||--o{ EVTDOS : declenche
    LIGNE ||--o{ EVTDOS : impacte

    DOSSIER {
        string cleofs PK "Clé partielle"
        string numero_dossier
        string client_id FK
        decimal montant_demande
        decimal montant_approuve
        string statut_dossier
        date date_ouverture
        date date_fermeture
    }

    LIGNE {
        string cleofs FK
        int numero_ligne PK
        decimal montant_nominal
        decimal montant_utilise
        decimal montant_restant
        date date_mise_en_place
        string type_ligne
    }

    REVOLVING {
        string cleofs FK
        int numero_ligne FK
        decimal plafond_initial
        decimal plafond_actuel
        date date_depuis
    }

    ECHIMP {
        string cleofs FK
        int numero_ligne FK
        int numero_echance PK
        decimal montant_principal
        decimal montant_interet
        date date_echance_prevue
        string statut_impaye
    }

    EVTDOS {
        string cleofs FK
        int numero_evenement PK
        string type_evenement
        date date_evenement
        string utilisateur
    }
```

---

## Cycle de Vie d'un Dossier

```mermaid
stateDiagram-v2
    [*] --> CREATION: Demande crédit
    CREATION --> INSTRUCTION: Dossier complet
    INSTRUCTION --> DECISION: Analyse complète
    DECISION --> APPROUVE: Accord
    DECISION --> REJETE: Refus
    APPROUVE --> ENCOURS: Déblocage fonds
    ENCOURS --> REMBOURSEMENT: Paiements reçus
    REMBOURSEMENT --> CLOS: Dossier soldé
    REJETE --> [*]
    CLOS --> [*]
    
    ENCOURS --> SINISTRE: Retard +90j
    SINISTRE --> RECOUVREMENT: Action légale
    RECOUVREMENT --> CLOS
```

---

## Notes Importantes pour le RAG

### Clés pour Recherche

- **Clé Partielle**: CLEOFS identifie TOUS les enregistrements du dossier
- **Relations**: DOSSIER → LIGNE → ECHIMP (hiérarchie)
- **Événements**: EVTDOS suit toutes les modifications

### Enregistrements et Codes

Chaque table est identifiée par:
- `ENR-DGEN`: Dossier général
- `ENR-DLIGN`: Lignes de crédit
- `ENR-DREV`: Revolving
- `ENR-ECHIMP`: Échéances impayées
- `ENR-EVTDOS`: Événements

### Indicateurs & Flags

**Très nombreux** dans LS V3.8.0:
- Indicateurs saisie (voir ci-après)
- Indicateurs édition des lettres
- Flags statutaires (I : oui, blanc : non)
- Codes groupe (données resultates)
- Indicateurs présence phase initiale

### Questions Typiques pour RAG

```
Q: "État du dossier ABC123?"
→ Cherche DOSSIER.cleofs=ABC123 + DOSSIER.statut_dossier

Q: "Échéances impayées?"
→ Cherche ECHIMP avec ECHIMP.statut_impaye

Q: "Historique modifications?"
→ Cherche EVTDOS.cleofs=ABC123 ordre chrono

Q: "Lignes de crédit actives?"
→ Cherche LIGNE.cleofs=ABC123 + statut
```

---

**Version du document:** V1.00 du 22/01/2021  
**Source:** LS - V3.8.0 - C.01.02 - Intégration - Description des prises  
**Créateur:** Sopra Banking Software
