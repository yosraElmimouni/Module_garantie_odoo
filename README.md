# Module Odoo - Gestion des Garanties

## Description

Ce module Odoo permet de gérer les garanties des produits . Il offre une interface complète pour enregistrer, suivre et gérer l'état des garanties de vos clients.

## Fonctionnalités

Le module **Gestion des Garanties** inclut les fonctionnalités suivantes :

- **Création de garanties** : Enregistrez les garanties pour chaque produit vendu avec tous les détails nécessaires.
- **Suivi des dates** : Calcul automatique de la date d'expiration basée sur la date d'achat et la durée de la garantie.
- **Gestion des statuts** : Gérez l'état de chaque garantie (Brouillon, Valide, Expirée, Réclamation en cours).
- **Réclamations** : Créez et suivez les réclamations associées aux garanties.
- **Filtres et recherches** : Recherchez facilement les garanties par client, produit ou statut.

## Structure du Module

```
gestion_garantie_odoo/
├── __init__.py              # Fichier d'initialisation du module
├── __manifest__.py          # Métadonnées du module (nom, version, dépendances)
├── models/
│   ├── __init__.py          # Fichier d'initialisation du package models
│   └── models.py            # Définition du modèle de garantie
├── views/
│   └── views.xml            # Définition des vues (formulaire, liste, menu)
└── README.md                # Ce fichier
```

## Modèle de Données

Le modèle `gestion.garantie` contient les champs suivants :

| Champ | Type | Description |
| :--- | :--- | :--- |
| **Numéro de Garantie** | Char | Identifiant unique généré automatiquement |
| **Client** | Many2one | Lien vers le client (res.partner) |
| **Produit** | Many2one | Lien vers le produit (product.product) |
| **Numéro de Série** | Char | Numéro de série unique du produit |
| **Date d'Achat** | Date | Date de l'achat du produit |
| **Durée de Garantie** | Integer | Durée en mois (par défaut 12) |
| **Date d'Expiration** | Date | Calculée automatiquement |
| **Statut** | Selection | Brouillon, Valide, Expirée, Réclamation en cours |
| **Description du Problème** | Text | Description du défaut en cas de réclamation |

## Installation

### Prérequis

- Odoo 14.0 ou supérieur
- Accès administrateur à votre instance Odoo
- Les modules de base : `base`, `sale`

### Étapes d'installation

1. **Placer le module** : Copiez le dossier `gestion_garantie_odoo` dans le répertoire `addons` de votre installation Odoo.

   ```bash
   cp -r gestion_garantie_odoo /chemin/vers/odoo/addons/
   ```

2. **Actualiser la liste des modules** : Dans Odoo, allez dans **Applications** → **Mettre à jour la liste des modules**.

3. **Installer le module** : Recherchez "Gestion des Garanties" dans la liste des modules disponibles et cliquez sur **Installer**.

4. **Vérifier l'installation** : Après l'installation, un nouveau menu **Gestion des Garanties** devrait apparaître dans le menu principal.

## Utilisation

### Créer une Garantie

1. Allez dans **Gestion des Garanties** → **Garanties**.
2. Cliquez sur **Créer** pour créer une nouvelle garantie.
3. Remplissez les champs obligatoires :
   - **Client** : Sélectionnez le client
   - **Produit** : Sélectionnez le produit
   - **Numéro de Série** : Entrez le numéro de série
   - **Date d'Achat** : Sélectionnez la date d'achat
   - **Durée de Garantie** : Entrez la durée en mois
4. Cliquez sur **Enregistrer**.

### Valider une Garantie

1. Ouvrez la garantie à valider.
2. Cliquez sur le bouton **Valider** pour passer le statut à "Valide".

### Créer une Réclamation

1. Ouvrez la garantie concernée.
2. Décrivez le problème dans le champ **Description du Problème**.
3. Cliquez sur **Créer Réclamation** pour passer le statut à "Réclamation en cours".

### Marquer une Garantie comme Expirée

1. Ouvrez la garantie.
2. Cliquez sur **Marquer Expirée** pour passer le statut à "Expirée".

### Réinitialiser une Garantie

1. Ouvrez la garantie.
2. Cliquez sur **Réinitialiser** pour revenir au statut "Brouillon".

## Vues Disponibles

Le module fournit deux vues principales :

- **Vue Arborescence (Tree View)** : Affiche toutes les garanties dans un tableau avec les informations principales (numéro, client, produit, numéro de série, dates, statut).
- **Vue Formulaire** : Affiche les détails complets d'une garantie avec tous les champs et les boutons d'action.

## Dépendances

Le module dépend des modules Odoo suivants :

- `base` : Module de base d'Odoo
- `sale` : Module de gestion des ventes

## Personnalisation

Vous pouvez personnaliser ce module selon vos besoins :

- **Ajouter des champs** : Modifiez le fichier `models/models.py` pour ajouter de nouveaux champs.
- **Modifier les vues** : Éditez le fichier `views/views.xml` pour changer l'apparence des formulaires et listes.
- **Ajouter des actions** : Créez de nouvelles méthodes dans le modèle pour des actions personnalisées.


---
  
**Groupe** : 
  - Oumaima Mellah 
  - Imane Bouhabba 
  - Yosra El mimouni  


# fkyipazawkxhzykt