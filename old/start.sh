#!/bin/bash

# Script de démarrage de l'application Cinema Palace

echo "🎬 Démarrage de Cinema Palace..."

# Vérifier si MySQL est démarré
echo "Vérification de MySQL..."
if ! pgrep -x "mysqld" > /dev/null; then
    echo "❌ MySQL n'est pas démarré. Veuillez démarrer MySQL d'abord."
    echo "Sur macOS avec Homebrew: brew services start mysql"
    exit 1
fi

echo "✅ MySQL est démarré"

# Démarrer l'application Flask
echo "🚀 Démarrage du serveur Flask..."
export FLASK_APP=server.py
export FLASK_ENV=development

# Utiliser l'environnement virtuel
source path/to/venv/bin/activate

python server.py
