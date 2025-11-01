# Guide d'Installation - Module Odoo Gestion des Garanties

## Prérequis

- **Odoo 14.0** ou supérieur (compatible jusqu'à Odoo 17)
- Accès **administrateur** à votre instance Odoo
- Les modules de base : `base` et `sale` (généralement déjà installés)

## Méthode 1 : Installation via Fichier ZIP (Recommandée)

### Étape 1 : Extraire le module

1. Téléchargez l'archive `gestion_garantie_odoo.zip`
2. Décompressez-la dans le répertoire `addons` de votre Odoo :

```bash
unzip gestion_garantie_odoo.zip -d /chemin/vers/odoo/addons/
```

Ou manuellement :
- Copiez le dossier `gestion_garantie_odoo` dans votre répertoire `addons`

### Étape 2 : Actualiser la liste des modules

1. Connectez-vous à Odoo en tant qu'administrateur
2. Allez dans **Applications** (menu supérieur)
3. Cliquez sur **Mettre à jour la liste des modules** (bouton en haut à droite)
4. Attendez le rechargement de la page

### Étape 3 : Installer le module

1. Recherchez "**Gestion des Garanties**" dans la barre de recherche
2. Cliquez sur le module trouvé
3. Cliquez sur le bouton **Installer**
4. Attendez la fin de l'installation

### Étape 4 : Vérifier l'installation

Après l'installation, vous devriez voir un nouveau menu **Gestion des Garanties** dans le menu principal.

---

## Méthode 2 : Installation via Ligne de Commande

Si vous avez accès au serveur Odoo :

```bash
# Copier le module dans le répertoire addons
cp -r gestion_garantie_odoo /chemin/vers/odoo/addons/

# Redémarrer Odoo
sudo systemctl restart odoo

# Ou si vous utilisez Docker
docker restart odoo-container
```

Puis installez le module via l'interface Odoo (Étapes 2-4 ci-dessus).

---

## Vérification de l'Installation

### Vérifier que le module est bien installé

1. Allez dans **Applications** → **Modules installés**
2. Recherchez "Gestion des Garanties"
3. Le module doit apparaître avec le statut **Installé**

### Accéder au module

1. Cliquez sur le menu **Gestion des Garanties** dans le menu principal
2. Cliquez sur **Garanties** pour voir la liste
3. Cliquez sur **Créer** pour ajouter une nouvelle garantie

---

## Dépannage

### Le module n'apparaît pas dans la liste

- **Solution 1** : Cliquez sur **Mettre à jour la liste des modules** et attendez
- **Solution 2** : Vérifiez que le dossier `gestion_garantie_odoo` est bien dans le répertoire `addons`
- **Solution 3** : Vérifiez que le fichier `__manifest__.py` est présent et bien formaté

### Erreur lors de l'installation

- **Erreur de dépendances** : Assurez-vous que les modules `base` et `sale` sont installés
- **Erreur de syntaxe** : Vérifiez que les fichiers Python sont bien encodés en UTF-8
- **Erreur de permissions** : Vérifiez que vous avez les droits d'administrateur

### Le menu n'apparaît pas après l'installation

- Rechargez la page (F5)
- Déconnectez-vous et reconnectez-vous
- Redémarrez le serveur Odoo

---

## Configuration Initiale

### Créer la première garantie

1. Allez dans **Gestion des Garanties** → **Garanties**
2. Cliquez sur **Créer**
3. Remplissez les champs obligatoires :
   - **Client** : Sélectionnez un client existant
   - **Produit** : Sélectionnez un produit
   - **Numéro de Série** : Entrez un numéro unique
   - **Date d'Achat** : Sélectionnez la date
   - **Durée de Garantie** : Entrez le nombre de mois
4. Cliquez sur **Enregistrer**
5. Cliquez sur **Valider** pour activer la garantie

---

## Désinstallation

Si vous souhaitez désinstaller le module :

1. Allez dans **Applications** → **Modules installés**
2. Recherchez "Gestion des Garanties"
3. Cliquez sur le module
4. Cliquez sur **Désinstaller**

**Note** : Les données des garanties seront conservées dans la base de données.

---

## Support

Pour toute question ou problème :

1. Consultez le fichier `README.md` pour plus de détails sur les fonctionnalités
2. Vérifiez les logs Odoo : `/var/log/odoo/odoo.log`
3. Contactez votre administrateur Odoo

---

**Version du module** : 1.0  
**Date de création** : 31 octobre 2025  
**Compatibilité** : Odoo 14.0+
