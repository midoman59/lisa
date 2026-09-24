# LS V3.8.0 - Schémas Exacts de Base de Données

Basé sur **LS - V3.8.0 - C.01.02 - Description des prises - Fichiers permanents** (346 pages)

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

Structure principale pour chaque dossier de crédit.

### Champs Clés

| Position | Code Champ | Type | Taille | Description | Enregistrement |
|----------|-----------|------|--------|-------------|-----------------|
| 1 | CLEOFS | X(00027) | 27 | Clé partielle | ENR-DGEN |
| 2 | IDDOSRG | X(00005) | 5 | Identifiant de l'enregistrement | |
| 3 | NOENREG | 99(00009) | 9 | Numéro d'occurrence du bloc | |
| 4 | OPFLDRO1 | X(00037) | 37 | Zone de groupe | |

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
