#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des fonctions CRUD nouvellement ajoutées
"""
import modele

def test_movie_crud():
    """Test des opérations CRUD pour les films"""
    print("=== Test des films ===")
    
    # Test d'ajout avec les nouveaux champs
    print("Ajout d'un film de test...")
    success, message = modele.add_movie(
        name="Film Test CRUD",
        duration=120,
        director="Réalisateur Test",
        cast="Acteur 1, Acteur 2",
        synopsis="Synopsis de test pour vérifier les nouveaux champs"
    )
    print(f"Ajout: {success} - {message}")
    
    # Récupérer tous les films pour trouver l'ID du film test
    movies = modele.get_all_movies()
    test_movie = None
    for movie in movies:
        if movie['name'] == "Film Test CRUD":
            test_movie = movie
            break
    
    if test_movie:
        print(f"Film créé avec ID: {test_movie['id']}")
        
        # Test de mise à jour
        print("Mise à jour du film...")
        success, message = modele.update_movie(
            test_movie['id'],
            name="Film Test CRUD Modifié",
            duration=130,
            director="Nouveau Réalisateur",
            cast="Nouveaux Acteurs",
            synopsis="Synopsis modifié"
        )
        print(f"Mise à jour: {success} - {message}")
        
        # Test de suppression
        print("Suppression du film...")
        success, message = modele.delete_movie(test_movie['id'])
        print(f"Suppression: {success} - {message}")
    
def test_room_crud():
    """Test des opérations CRUD pour les salles"""
    print("\n=== Test des salles ===")
    
    # Test d'ajout
    print("Ajout d'une salle de test...")
    success, message = modele.add_room("Salle Test CRUD", 5, 8)
    print(f"Ajout: {success} - {message}")
    
    # Récupérer toutes les salles pour trouver l'ID de la salle test
    rooms = modele.get_all_rooms()
    test_room = None
    for room in rooms:
        if room['name'] == "Salle Test CRUD":
            test_room = room
            break
    
    if test_room:
        print(f"Salle créée avec ID: {test_room['id']}")
        
        # Test de mise à jour
        print("Mise à jour de la salle...")
        success, message = modele.update_room(test_room['id'], "Salle Test CRUD Modifiée", 0, 0)
        print(f"Mise à jour: {success} - {message}")
        
        # Test de suppression
        print("Suppression de la salle...")
        success, message = modele.delete_room(test_room['id'])
        print(f"Suppression: {success} - {message}")

def test_showing_crud():
    """Test des opérations CRUD pour les séances"""
    print("\n=== Test des séances ===")
    
    # D'abord, s'assurer qu'il y a au moins un film et une salle
    movies = modele.get_all_movies()
    rooms = modele.get_all_rooms()
    
    if not movies or not rooms:
        print("Pas assez de données (films/salles) pour tester les séances")
        return
    
    movie_id = movies[0]['id']
    room_id = rooms[0]['id']
    
    # Test d'ajout
    print("Ajout d'une séance de test...")
    success, message = modele.add_showing(
        date="2025-12-31",
        starttime="20:00:00",
        baseprice=1200,  # 12.00€ en centimes
        room_id=room_id,
        movie_id=movie_id
    )
    print(f"Ajout: {success} - {message}")
    
    # Récupérer toutes les séances pour trouver l'ID de la séance test
    showings = modele.get_all_showings()
    test_showing = None
    for showing in showings:
        if showing['date'].strftime('%Y-%m-%d') == "2025-12-31" and str(showing['starttime']) == "20:00:00":
            test_showing = showing
            break
    
    if test_showing:
        print(f"Séance créée avec ID: {test_showing['id']}")
        
        # Test de mise à jour
        print("Mise à jour de la séance...")
        success, message = modele.update_showing(
            test_showing['id'],
            date="2025-12-31",
            starttime="21:00:00",
            baseprice=1500,  # 15.00€ en centimes
            room_id=room_id,
            movie_id=movie_id
        )
        print(f"Mise à jour: {success} - {message}")
        
        # Test de suppression
        print("Suppression de la séance...")
        success, message = modele.delete_showing(test_showing['id'])
        print(f"Suppression: {success} - {message}")

if __name__ == "__main__":
    print("Test des nouvelles fonctions CRUD")
    print("=" * 40)
    
    try:
        test_movie_crud()
        test_room_crud()
        test_showing_crud()
        print("\n✅ Tous les tests sont terminés !")
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()
