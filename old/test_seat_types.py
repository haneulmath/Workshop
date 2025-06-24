#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier les nouveaux types de sièges
"""

import old.modele as modele

def test_seat_types():
    """Teste les nouveaux types de sièges"""
    print("=== Test des nouveaux types de sièges ===\n")
    
    # Test 1: Créer une salle avec des sièges de différents types
    print("1. Création d'une salle de test...")
    success, message = modele.add_room("Test Seat Types", 30)
    print(f"Résultat: {message}")
    
    # Test 2: Récupérer les salles pour obtenir l'ID de la nouvelle salle
    rooms = modele.get_all_rooms()
    test_room = None
    for room in rooms:
        if room['name'] == "Test Seat Types":
            test_room = room
            break
    
    if test_room:
        print(f"Salle créée avec ID: {test_room['id']}")
        
        # Test 3: Afficher la disposition de la salle
        print(f"\n2. Disposition de la salle {test_room['id']}:")
        modele.print_room_layout(test_room['id'])
        
        # Test 4: Récupérer les sièges et compter par type
        layout = modele.get_room_layout(test_room['id'])
        if layout:
            type_counts = {'normal': 0, 'pmr': 0, 'stair': 0, 'empty': 0}
            total_seats = 0
            
            for row_letter, seats in layout.items():
                for seat in seats:
                    seat_type = seat['type']
                    if seat_type in type_counts:
                        type_counts[seat_type] += 1
                    total_seats += 1
            
            print(f"\n3. Statistiques des sièges:")
            print(f"Total de sièges: {total_seats}")
            for seat_type, count in type_counts.items():
                print(f"- {seat_type.upper()}: {count}")
    
    print("\n=== Test terminé ===")

def test_seance_seats_api():
    """Teste l'API de récupération des sièges pour une séance"""
    print("\n=== Test de l'API des sièges ===\n")
    
    # Récupérer toutes les séances
    seances = modele.get_all_seances()
    if seances and len(seances) > 0:
        test_seance = seances[0]
        print(f"Test avec la séance: {test_seance['movie_name']} - {test_seance['starttime']}")
        
        # Récupérer les sièges
        seats = modele.get_seats_for_seance(test_seance['id'])
        if seats:
            print(f"Nombre de sièges récupérés: {len(seats)}")
            
            # Analyser les types
            type_counts = {}
            for seat in seats:
                seat_type = seat['type']
                if seat_type in type_counts:
                    type_counts[seat_type] += 1
                else:
                    type_counts[seat_type] = 1
            
            print("Répartition par type:")
            for seat_type, count in type_counts.items():
                print(f"- {seat_type}: {count}")
            
            # Afficher quelques exemples
            print("\nExemples de sièges:")
            for i, seat in enumerate(seats[:5]):
                print(f"- {seat['seat_row']}{seat['seat_column']}: type={seat['type']}, occupé={seat['occupied']}")
        else:
            print("Erreur: aucun siège récupéré")
    else:
        print("Erreur: aucune séance trouvée")

if __name__ == "__main__":
    test_seat_types()
    test_seance_seats_api()
