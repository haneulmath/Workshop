# 🎬 Cinema Palace - Système de Réservation

Une application Flask complète pour la gestion d'un cinéma avec réservation de places en ligne.

## Fonctionnalités

### Interface Utilisateur
- **Authentification simple** : Connexion avec nom d'utilisateur et mot de passe
- **Sélection de films** : Affichage des séances du jour avec horaires et salles
- **Réservation de places** : Interface graphique pour choisir ses sièges
- **Gestion des spectateurs** : Informations détaillées pour chaque siège réservé
- **Tarification automatique** : Prix calculé selon l'âge (enfant, adulte, senior)

### Interface d'Administration
- **Gestion des films** : Ajouter des films avec nom et durée
- **Gestion des salles** : Créer des salles avec capacité automatique des sièges
- **Gestion des séances** : Programmer les séances avec date, heure, prix, salle et film
- **Vue d'ensemble** : Tableau de bord avec toutes les données

## Structure de la Base de Données

L'application utilise le schéma défini dans `V1.sql` avec les tables suivantes :
- `account` : Comptes utilisateurs
- `movie` : Films disponibles
- `room` : Salles de cinéma
- `seat` : Sièges de chaque salle (avec support PMR)
- `seance` : Séances programmées
- `booking` : Réservations
- `customer` : Spectateurs
- `seatreservation` : Association spectateur-siège-séance
- `ageprice` : Tarifs selon l'âge

## Installation et Configuration

### Prérequis
- Python 3.8+
- MySQL Server
- Un environnement virtuel Python (recommandé)

### Installation

1. **Cloner le projet** (si applicable)
```bash
cd "Architecture et logicielle/Workshop"
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Sur macOS/Linux
# ou
venv\Scripts\activate  # Sur Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer MySQL**
   - Assurez-vous que MySQL est démarré
   - Créez une base de données nommée `Cinemacousas` (ou modifiez `DB_CONFIG` dans `modele.py`)
   - Vérifiez les paramètres de connexion dans `modele.py` :
     ```python
     DB_CONFIG = {
         "host": "localhost",
         "user": "root",
         "password": "root",  # Ajustez selon votre configuration
         "database": "Cinemacousas"
     }
     ```

### Démarrage

1. **Démarrer MySQL** (si pas déjà fait)
```bash
# Sur macOS avec Homebrew
brew services start mysql

# Ou démarrer manuellement selon votre installation
```

2. **Lancer l'application**
```bash
python server.py
```

L'application sera accessible à l'adresse : http://localhost:5000

## Utilisation

### Interface Client (http://localhost:5000)
1. **Connexion** : Utilisez n'importe quel nom d'utilisateur avec un mot de passe non vide
2. **Sélection du film** : Cliquez sur une séance disponible
3. **Réservation** : 
   - Cliquez sur les sièges disponibles (gris)
   - Remplissez les informations du spectateur pour chaque siège
   - Validez votre commande

### Interface d'Administration (http://localhost:5000/admin)
1. **Ajouter des films** : Nom et durée en minutes
2. **Créer des salles** : Nom et capacité (les sièges sont créés automatiquement)
3. **Programmer des séances** : Date, heure, prix, salle et film

## Structure des Fichiers

```
Workshop/
├── server.py              # Serveur Flask principal
├── modele.py             # Gestion de la base de données
├── V1.sql               # Schéma de base de données
├── requirements.txt     # Dépendances Python
├── start.sh            # Script de démarrage
├── templates/
│   ├── index.html      # Interface client
│   └── admin.html      # Interface d'administration
└── img/                # Assets (images de sièges)
```

## API Endpoints

### Authentification
- `POST /login` : Connexion utilisateur
- `GET /logout` : Déconnexion

### API Client
- `GET /api/seances/today` : Séances du jour
- `GET /api/seance/<id>/seats` : Sièges d'une séance
- `POST /api/booking` : Créer une réservation

### Administration
- `POST /admin/movie` : Ajouter un film
- `POST /admin/room` : Ajouter une salle
- `POST /admin/seance` : Ajouter une séance

## Données de Test

Au premier démarrage, l'application insère automatiquement :
- 2 comptes utilisateurs (admin@cinema.com / user@cinema.com)
- 3 salles (Salle 1, Salle 2, Salle VIP)
- 3 films (Dune: Part Two, The Creator, Oppenheimer)
- 5 séances pour les 24-25 juin 2025
- Sièges automatiques pour chaque salle (avec sièges PMR)
- Tarifs par âge (Enfant: -30%, Adulte: prix normal, Senior: -20%)

## Notes Techniques

- **Sécurité** : L'authentification est simplifiée pour la démonstration
- **Prix** : Stockés en centimes dans la base de données
- **Sièges PMR** : Les 2 premiers sièges de chaque première rangée
- **Auto-génération** : Les sièges sont créés automatiquement lors de l'ajout d'une salle
- **Grille des sièges** : Organisation en rangées de 10 sièges maximum

## Développement

Pour étendre l'application :
1. Ajouter de nouvelles routes dans `server.py`
2. Créer les fonctions correspondantes dans `modele.py`
3. Mettre à jour les templates HTML si nécessaire
4. Tester les nouvelles fonctionnalités

## Troubleshooting

**Erreur de connexion MySQL** :
- Vérifiez que MySQL est démarré
- Contrôlez les paramètres dans `DB_CONFIG`
- Assurez-vous que la base de données `Cinemacousas` existe

**Erreur 404 sur les templates** :
- Vérifiez que le dossier `templates/` existe
- Assurez-vous que les fichiers HTML sont présents

**Erreur d'importation** :
- Activez l'environnement virtuel
- Réinstallez les dépendances : `pip install -r requirements.txt`
