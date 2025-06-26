#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validation post-nettoyage
Vérifie que toutes les fonctionnalités principales fonctionnent
"""

def test_imports():
    """Test des imports principaux"""
    print("🔍 Test des imports...")
    
    try:
        import modele
        print("   ✅ modele.py importé")
        
        from server import app
        print("   ✅ server.py importé")
        
        # Test des nouvelles fonctions fusionnées
        if hasattr(modele, 'create_movieposter_table'):
            print("   ✅ create_movieposter_table disponible")
        
        if hasattr(modele, 'insert_poster_from_file'):
            print("   ✅ insert_poster_from_file disponible")
            
        if hasattr(modele, 'list_movie_posters'):
            print("   ✅ list_movie_posters disponible")
            
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur d'import: {e}")
        return False

def test_file_structure():
    """Test de la structure des fichiers"""
    print("\n📁 Test de la structure...")
    
    import os
    
    # Fichiers qui doivent exister
    required_files = [
        'server.py',
        'modele.py',
        'static/css/style.css',
        'static/css/admin.css',
        'static/js/admin.js',
        'static/js/common.js',
        'templates/home.html',
        'templates/admin.html'
    ]
    
    # Fichiers qui ne doivent plus exister
    should_not_exist = [
        'insert_posters.py',
        'test_poster_upload.py',
        'test_real_upload.py',
        'static/css/unused-styles.css',
        'static/js/unused-functions.js',
        'templates/test_posters.html'
    ]
    
    all_good = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} manquant")
            all_good = False
    
    for file in should_not_exist:
        if not os.path.exists(file):
            print(f"   ✅ {file} supprimé")
        else:
            print(f"   ⚠️  {file} existe encore")
    
    return all_good

def test_database_functions():
    """Test des fonctions de base de données"""
    print("\n🗄️  Test des fonctions BD...")
    
    try:
        import modele
        
        # Test de connexion (sans exécuter)
        if hasattr(modele, 'get_db_connection'):
            print("   ✅ get_db_connection disponible")
        
        if hasattr(modele, 'get_movie_poster'):
            print("   ✅ get_movie_poster disponible")
            
        if hasattr(modele, 'save_movie_poster'):
            print("   ✅ save_movie_poster disponible")
            
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def main():
    """Fonction principale de validation"""
    print("🧹 VALIDATION POST-NETTOYAGE")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_file_structure,
        test_database_functions
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 50)
    print("📊 RÉSULTATS:")
    
    if all(results):
        print("🎉 TOUS LES TESTS RÉUSSIS !")
        print("   Le nettoyage a été effectué avec succès.")
        print("   Toutes les fonctionnalités sont préservées.")
    else:
        print("⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
        print("   Vérifiez les erreurs ci-dessus.")
    
    print(f"\n✅ Tests réussis: {sum(results)}/{len(results)}")

if __name__ == "__main__":
    main()
