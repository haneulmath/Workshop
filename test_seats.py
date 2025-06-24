#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour démontrer la création automatique de sièges
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

import old.modele as modele

def test_room_creation():
    """Test de création d'une salle avec génération automatique des sièges"""
    
    print("=== Test de création d'une salle ===\n")
    
    # Test 1: Petite salle (15 sièges)
    print("1. Création d'une petite salle (15 sièges)")
    success, message = modele.add_room("Salle Test 1", 15)
    print(f"Résultat: {message}")
    
    if success:
        # Récupérer l'ID de la salle créée
        rooms = modele.get_all_rooms()
        if rooms:
            test_room_id = None
            for room in rooms:
                if room['name'] == "Salle Test 1":
                    test_room_id = room['id']
                    break
            
            if test_room_id:
                print(f"\nDisposition de la salle créée (ID: {test_room_id}):")
                modele.print_room_layout(test_room_id)
    
    print("\n" + "="*50 + "\n")
    
    # Test 2: Salle moyenne (25 sièges)
    print("2. Création d'une salle moyenne (25 sièges)")
    success, message = modele.add_room("Salle Test 2", 25)
    print(f"Résultat: {message}")
    
    if success:
        rooms = modele.get_all_rooms()
        if rooms:
            test_room_id = None
            for room in rooms:
                if room['name'] == "Salle Test 2":
                    test_room_id = room['id']
                    break
            
            if test_room_id:
                print(f"\nDisposition de la salle créée (ID: {test_room_id}):")
                modele.print_room_layout(test_room_id)

def explain_seat_generation():
    """Explique le processus de génération des sièges"""
    
    print("=== Explication du processus de génération des sièges ===\n")
    
    print("Quand un administrateur crée une salle via l'interface admin:")
    print("1. L'utilisateur saisit le nom de la salle et sa capacité")
    print("2. Le serveur Flask appelle modele.add_room(name, capacity)")
    print("3. add_room() insère la salle dans la table 'room'")
    print("4. add_room() appelle automatiquement create_seats_for_room()")
    print("5. create_seats_for_room() génère tous les sièges:\n")
    
    capacities = [15, 25, 45]
    
    for capacity in capacities:
        seats_per_row = 10
        total_rows = (capacity + seats_per_row - 1) // seats_per_row
        
        print(f"   Exemple avec {capacity} sièges:")
        print(f"   - Rangées nécessaires: {total_rows}")
        
        seats_created = 0
        for row_num in range(1, total_rows + 1):
            seats_in_row = min(seats_per_row, capacity - seats_created)
            row_letter = chr(64 + row_num)
            print(f"   - Rangée {row_letter}: sièges {row_letter}1 à {row_letter}{seats_in_row}")
            seats_created += seats_in_row
        
        print(f"   - Total: {seats_created} sièges")
        print()
    
    print("Règles de génération:")
    print("- Maximum 10 sièges par rangée")
    print("- Rangées nommées A, B, C, D, ...")
    print("- Sièges numérotés 1, 2, 3, ... dans chaque rangée")
    print("- Les sièges A1 et A2 sont automatiquement marqués PMR")
    print("- Structure: seat_row (VARCHAR) + seat_column (INT)")

def show_database_structure():
    """Montre la structure de la table seat"""
    
    print("=== Structure de la table seat ===\n")
    
    print("Table: seat")
    print("├── id (INT, AUTO_INCREMENT, PRIMARY KEY)")
    print("├── pmr (TINYINT, 0=normal, 1=PMR)")
    print("├── room_id (INT, FOREIGN KEY vers room.id)")
    print("├── seat_row (VARCHAR(45), A, B, C, ...)")
    print("└── seat_column (INT, 1, 2, 3, ...)")
    print()
    print("Contrainte unique: (seat_row, seat_column, room_id)")
    print("→ Chaque combinaison lettre+numéro est unique par salle")
    print()
    print("Exemples de données:")
    print("| id | pmr | room_id | seat_row | seat_column |")
    print("|----|-----|---------|-------------|-------------|")
    print("| 1  | 1   | 1       | A           | 1           | ← PMR")
    print("| 2  | 1   | 1       | A           | 2           | ← PMR")
    print("| 3  | 0   | 1       | A           | 3           |")
    print("| 4  | 0   | 1       | A           | 4           |")
    print("| 5  | 0   | 1       | B           | 1           |")

if __name__ == "__main__":
    print("🎬 Test de génération automatique des sièges\n")
    
    # Vérifier la connexion
    if not modele.get_db_connection():
        print("❌ Impossible de se connecter à la base de données")
        sys.exit(1)
    
    print("✅ Connexion à la base de données réussie\n")
    
    # Expliquer le processus
    explain_seat_generation()
    print("\n" + "="*60 + "\n")
    
    # Montrer la structure
    show_database_structure()
    print("\n" + "="*60 + "\n")
    
    # Demander si on veut tester
    response = input("Voulez-vous tester la création de salles ? (y/n): ")
    if response.lower() in ['y', 'yes', 'o', 'oui']:
        test_room_creation()
    
    print("\n🎯 Résumé:")
    print("- Les sièges sont créés automatiquement lors de l'ajout d'une salle")
    print("- La fonction create_seats_for_room() gère la logique de génération")
    print("- Les lettres et numéros sont assignés selon une grille standard")
    print("- Les sièges PMR sont automatiquement définis (A1, A2)")
