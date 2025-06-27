# Cinemacousas - Système de Réservation de Cinéma

## 🚀 Démarrage rapide

```bash
# 1. Activer l'environnement virtuel (déjà configuré)
source cinemacousas_env/bin/activate

# 2. Lancer l'application
python3 server.py
```

L'application sera accessible à : `http://localhost:5000`

## Description
Application web Flask pour la gestion et réservation de séances de cinéma avec interface d'administration.

## Prérequis
- Python 3.8 ou supérieur
- MySQL/MariaDB server
- Un navigateur web moderne

## Installation

### 1. Cloner ou télécharger le projet
```bash
cd /chemin/vers/votre/dossier
# Le projet est déjà présent dans ce répertoire
```

### 2. Utiliser l'environnement virtuel

**L'environnement virtuel `cinemacousas_env` est déjà créé et configuré.**

Pour l'activer :
```bash
# Sur macOS/Linux
source cinemacousas_env/bin/activate

# Sur Windows
cinemacousas_env\Scripts\activate
```

Si vous devez recréer l'environnement virtuel :
```bash
python3 -m venv cinemacousas_env
source cinemacousas_env/bin/activate  # Sur macOS/Linux
pip install -r requirements.txt
```

### 3. Installer les dépendances (si nécessaire)

**Les dépendances sont déjà installées dans `cinemacousas_env`.**

Si vous devez les réinstaller :
```bash
# Assurez-vous que l'environnement virtuel est activé
source cinemacousas_env/bin/activate
pip install -r requirements.txt
```

## Dépendances utilisées

### Dépendances principales (requises)
- **Flask==3.0.0** - Framework web principal pour l'interface utilisateur
- **Flask-CORS==4.0.0** - Gestion des requêtes CORS pour l'API
- **mysql-connector-python==8.2.0** - Connecteur pour la base de données MySQL

### Dépendances automatiques (installées avec Flask)
Ces dépendances sont installées automatiquement avec Flask :
- `Werkzeug` - Serveur WSGI et utilitaires
- `Jinja2` - Moteur de templates pour le rendu HTML
- `MarkupSafe` - Échappement sécurisé pour les templates
- `itsdangerous` - Signature sécurisée des sessions
- `click` - Interface en ligne de commande
- `blinker` - Système de signaux

### Dépendances automatiques (installées avec mysql-connector)
- `protobuf` - Sérialisation des données pour MySQL

## Configuration de la base de données

### Paramètres de connexion
Les paramètres de connexion MySQL sont définis dans `modele.py` :
```python
DB_CONFIG = {
    "host": "82.66.24.184",
    "port": 3305,
    "user": "cinemacousas",
    "password": "password", 
    "database": "Cinemacousas"
}
```

### Scripts SQL
Les scripts de création de la base de données sont disponibles dans le dossier `workspace/` :
- `V1.sql` - Structure initiale
- `V2.sql` - Améliorations 
- `V3.sql` - Ajouts de fonctionnalités
- `V4.sql` - Version finale

## Lancement de l'application

### Méthode 1 : Avec l'environnement virtuel
```bash
# Activer l'environnement virtuel
source cinemacousas_env/bin/activate

# Lancer le serveur
python3 server.py
```

### Méthode 2 : Directement (si les dépendances sont installées globalement)
```bash
python3 server.py
```

L'application sera accessible à l'adresse : `http://localhost:5000`

## Structure du projet

```
Cinemacousas/
├── server.py              # Serveur Flask principal
├── modele.py              # Modèle de données et fonctions BDD
├── requirements.txt       # Dépendances Python
├── README.md             # Ce fichier
├── templates/            # Templates HTML Jinja2
├── static/              # Fichiers statiques (CSS, JS, images)
├── workspace/           # Scripts SQL et documentation
├── old/                # Archives et code de nettoyage
└── cinemacousas_env/   # Environnement virtuel (créé automatiquement)
```

## Fonctionnalités principales

- **Interface utilisateur** : Consultation des films et réservation de places
- **Interface administrateur** : Gestion des films, salles, séances et réservations
- **Gestion des sièges** : Support des places normales et PMR
- **Système de réservation** : Avec informations détaillées des spectateurs
- **Gestion des affiches** : Upload et affichage des posters de films

## Validation et tests

Pour vérifier que l'installation fonctionne :
```bash
source cinemacousas_env/bin/activate
python3 validate_cleanup.py
```

## Support

Ce projet utilise uniquement des dépendances stables et bien maintenues. En cas de problème :

1. Vérifiez que Python 3.8+ est installé : `python3 --version`
2. Vérifiez la connexion à la base de données MySQL
3. Assurez-vous que l'environnement virtuel est activé
4. Réinstallez les dépendances : `pip install -r requirements.txt --force-reinstall`

## Dernière mise à jour
Projet nettoyé et optimisé le 27 juin 2025.
