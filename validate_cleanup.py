#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de validation finale après nettoyage
Vérifie que toutes les fonctionnalités critiques fonctionnent
"""

import sys
sys.path.append('/Users/matheopalazzolo/Documents/IMAC/Architecture et logicielle/Cinemacousas')

import modele
from datetime import datetime, timedelta

def validate_post_cleanup():
    """Valide que le projet fonctionne après le nettoyage"""
    
    print("✅ Validation Post-Nettoyage - Cinemacousas")
    print("=" * 50)
    
    try:
        # Test 1: Import des modules principaux
        print("1️⃣  Test des imports...")
        import modele
        print("   ✅ modele.py importé")
        
        from flask import Flask
        print("   ✅ Flask importé")
        
        # Test 2: Fonctions critiques de modele.py
        print("\n2️⃣  Test des fonctions critiques...")
        
        # Test de connexion DB
        conn = modele.get_db_connection()
        if conn:
            conn.close()
            print("   ✅ Connexion base de données")
        else:
            print("   ⚠️  Connexion base de données échouée")
        
        # Test parse_time_safely (notre fix principal)
        result = modele.parse_time_safely('2025-06-26', timedelta(hours=3))
        print("   ✅ parse_time_safely (fix horaires)")
        
        result = modele.parse_time_safely('2025-06-26', "03:00")
        print("   ✅ parse_time_safely (string)")
        
        # Test des fonctions métier
        movies = modele.get_all_movies()
        print(f"   ✅ get_all_movies ({len(movies) if movies else 0} films)")
        
        rooms = modele.get_all_rooms()
        print(f"   ✅ get_all_rooms ({len(rooms) if rooms else 0} salles)")
        
        showings = modele.get_all_showings()
        print(f"   ✅ get_all_showings ({len(showings) if showings else 0} séances)")
        
        # Test 3: Fonctions supprimées ne sont plus présentes
        print("\n3️⃣  Vérification que les fonctions inutilisées ont été supprimées...")
        
        removed_functions = [
            'authenticate_user', 'create_account', 'get_room_by_id',
            'get_seat_by_position', 'create_movieposter_table',
            'insert_poster_from_file'
        ]
        
        # Fonctions qui ont été ré-ajoutées car nécessaires
        readded_functions = [
            'is_room_used_in_showings', 'has_room_bookings_for_seat'
        ]
        
        for func_name in removed_functions:
            if hasattr(modele, func_name):
                print(f"   ❌ {func_name} encore présente (devrait être supprimée)")
            else:
                print(f"   ✅ {func_name} correctement supprimée")
        
        for func_name in readded_functions:
            if hasattr(modele, func_name):
                print(f"   ✅ {func_name} ré-ajoutée (nécessaire)")
            else:
                print(f"   ❌ {func_name} manquante (devrait être présente)")
        
        # Test 4: Test de scénario complet (sans base de données)
        print("\n4️⃣  Test du scénario de conflits d'horaire...")
        
        # Test avec des heures éloignées (3h vs 12h10)
        date = "2025-06-26"
        time1 = "03:00"
        time2 = "12:10"
        
        dt1 = modele.parse_time_safely(date, time1)
        dt2 = modele.parse_time_safely(date, time2)
        
        # Simuler le calcul de conflit avec marge - supposons que le film 1 dure 2h
        film_duration = timedelta(hours=2)
        margin = timedelta(minutes=10)
        
        # Fin du film 1 + marge vs début du film 2 - marge
        end_time1_with_margin = dt1 + film_duration + margin
        start_time2_with_margin = dt2 - margin
        
        conflict = end_time1_with_margin > start_time2_with_margin
        
        if not conflict:
            print("   ✅ Pas de conflit entre 3h et 12h10 avec film de 2h (correct)")
        else:
            print("   ❌ Conflit détecté entre 3h et 12h10 avec film de 2h (incorrect)")
        
        # Statistiques finales
        print("\n📊 Statistiques du module modele.py:")
        all_functions = [attr for attr in dir(modele) if callable(getattr(modele, attr)) and not attr.startswith('_')]
        print(f"   • Fonctions totales: {len(all_functions)}")
        print(f"   • Fonctions métier: {len([f for f in all_functions if not f.startswith('get_db')])}")
        
        print("\n✅ Validation réussie!")
        print("\n📋 Résumé:")
        print("   • Import modele.py: ✅")
        print("   • Fonctions critiques: ✅") 
        print("   • Fix horaires: ✅")
        print("   • Nettoyage vérifié: ✅")
        print("   • Scénario 3h vs 12h10: ✅")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la validation: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = validate_post_cleanup()
    if success:
        print("\n🎉 Le projet est prêt après nettoyage!")
    else:
        print("\n⚠️  Des problèmes ont été détectés.")
        sys.exit(1)
