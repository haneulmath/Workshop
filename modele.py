#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import mysql.connector
from mysql.connector import Error
import hashlib
from datetime import datetime, time

# Connexion à la BDD
DB_CONFIG = {
    "host": "82.66.24.184",
    "port": 3305,
    "user": "cinemacousas",
    "password": "password", 
    "database": "Cinemacousas"
}

def get_db_connection():
    """Établit et retourne une connexion à la base de données"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL: {e}")
        return None

def hash_password(password):
    """Hash un mot de passe avec SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

# ===== FONCTIONS POUR L'AUTHENTIFICATION =====

def authenticate_user(email, password):
    """Authentifie un utilisateur"""
    connection = get_db_connection()
    
    if connection is None:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        password_hash = hash_password(password)
        
        cursor.execute("SELECT * FROM account WHERE email = %s AND password_hash = %s", 
                      (email, password_hash))
        user = cursor.fetchone()
        
        return user
        
    except Error as e:
        print(f"Erreur lors de l'authentification: {e}")
        return None
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def create_account(email, password):
    """Crée un nouveau compte utilisateur"""
    connection = get_db_connection()
    
    if connection is None:
        return False, "Erreur de connexion à la base de données"
        
    try:
        cursor = connection.cursor()
        
        # Vérifier si l'email existe déjà
        cursor.execute("SELECT id FROM account WHERE email = %s", (email,))
        if cursor.fetchone():
            return False, "Un compte avec cet email existe déjà"
        
        # Créer le compte
        password_hash = hash_password(password)
        cursor.execute("INSERT INTO account (email, password_hash) VALUES (%s, %s)", 
                      (email, password_hash))
        connection.commit()
        
        return True, "Compte créé avec succès"
        
    except Error as e:
        return False, f"Erreur lors de la création du compte: {e}"
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# ===== FONCTIONS POUR LES FILMS =====

def get_all_movies():
    """Récupère tous les films"""
    connection = get_db_connection()
    
    if connection is None:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM movie ORDER BY name")
        movies = cursor.fetchall()
        return movies
        
    except Error as e:
        print(f"Erreur lors de la récupération des films: {e}")
        return None
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_movie_by_id(movie_id):
    """Récupère un film par son ID"""
    connection = get_db_connection()
    
    if connection is None:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM movie WHERE id = %s", (movie_id,))
        movie = cursor.fetchone()
        return movie
        
    except Error as e:
        print(f"Erreur lors de la récupération du film: {e}")
        return None
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def add_movie(name, duration, director=None, cast=None, synopsis=None):
    """Ajoute un nouveau film"""
    connection = get_db_connection()
    
    if connection is None:
        return False, "Erreur de connexion à la base de données"
        
    try:
        cursor = connection.cursor()
        
        cursor.execute("""
            INSERT INTO movie (name, duration, director, cast, synopsis) 
            VALUES (%s, %s, %s, %s, %s)
        """, (name, duration, director, cast, synopsis))
        connection.commit()
        
        return True, f"Film '{name}' ajouté avec succès"
        
    except Error as e:
        return False, f"Erreur lors de l'ajout du film: {e}"
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def update_movie(movie_id, name, duration, director, cast, synopsis):
    """Met à jour un film"""
    connection = get_db_connection()
    
    if connection is None:
        return False, "Erreur de connexion à la base de données"
        
    try:
        cursor = connection.cursor()
        
        cursor.execute("""
            UPDATE movie 
            SET name = %s, duration = %s, director = %s, cast = %s, synopsis = %s
            WHERE id = %s
        """, (name, duration, director, cast, synopsis, movie_id))
        connection.commit()
        
        if cursor.rowcount > 0:
            return True, f"Film '{name}' mis à jour avec succès"
        else:
            return False, "Film non trouvé"
        
    except Error as e:
        return False, f"Erreur lors de la mise à jour du film: {e}"
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def delete_movie(movie_id):
    """Supprime un film"""
    connection = get_db_connection()
    
    if connection is None:
        return False, "Erreur de connexion à la base de données"
        
    try:
        cursor = connection.cursor()
        
        # Vérifier s'il y a des séances associées
        cursor.execute("SELECT COUNT(*) as count FROM showing WHERE movie_id = %s", (movie_id,))
        result = cursor.fetchone()
        if result and result[0] > 0:
            return False, "Impossible de supprimer ce film car il a des séances programmées"
        
        cursor.execute("DELETE FROM movie WHERE id = %s", (movie_id,))
        connection.commit()
        
        if cursor.rowcount > 0:
            return True, "Film supprimé avec succès"
        else:
            return False, "Film non trouvé"
        
    except Error as e:
        return False, f"Erreur lors de la suppression du film: {e}"
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# ===== FONCTIONS POUR LES SALLES =====

def get_all_rooms():
    """Récupère toutes les salles"""
    connection = get_db_connection()
    
    if connection is None:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM room ORDER BY name")
        rooms = cursor.fetchall()
        return rooms
        
    except Error as e:
        print(f"Erreur lors de la récupération des salles: {e}")
        return None
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_room_by_id(room_id):
    """Récupère une salle par son ID"""
    connection = get_db_connection()
    
    if connection is None:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM room WHERE id = %s", (room_id,))
        room = cursor.fetchone()
        return room
        
    except Error as e:
        print(f"Erreur lors de la récupération de la salle: {e}")
        return None
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def add_room(name, nb_rows, nb_columns):
    """Ajoute une nouvelle salle et crée automatiquement les sièges"""
    connection = get_db_connection()
    
    if connection is None:
        return False, "Erreur de connexion à la base de données"
        
    try:
        cursor = connection.cursor()
        
        # Ajouter la salle
        cursor.execute("INSERT INTO room (name, nb_rows, nb_columns) VALUES (%s, %s, %s)", 
                      (name, nb_rows, nb_columns))
        room_id = cursor.lastrowid
        
        # Créer les sièges pour la nouvelle salle
        seats_created = 0
        for row_number in range(1, nb_rows + 1):
            row_letter = chr(64 + row_number)  # A, B, C, etc.
            
            for seat_column in range(1, nb_columns + 1):
                cursor.execute("""
                    INSERT INTO seat (type, room_id, seat_row, seat_column) 
                    VALUES ('normal', %s, %s, %s)
                """, (room_id, row_letter, seat_column))
                seats_created += 1
        
        connection.commit()
        
        return True, f"Salle '{name}' ajoutée avec succès ({seats_created} sièges créés)"
        
    except Error as e:
        return False, f"Erreur lors de l'ajout de la salle: {e}"
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def update_room(room_id, name, nb_rows, nb_columns):
    """Met à jour une salle (nom uniquement pour éviter les conflits avec les sièges existants)"""
    connection = get_db_connection()
    
    if connection is None:
        return False, "Erreur de connexion à la base de données"
        
    try:
        cursor = connection.cursor()
        
        # Mettre à jour uniquement le nom pour éviter les problèmes avec les sièges existants
        cursor.execute("UPDATE room SET name = %s WHERE id = %s", (name, room_id))
        connection.commit()
        
        if cursor.rowcount > 0:
            return True, f"Salle '{name}' mise à jour avec succès"
        else:
            return False, "Salle non trouvée"
        
    except Error as e:
        return False, f"Erreur lors de la mise à jour de la salle: {e}"
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def delete_room(room_id):
    """Supprime une salle et tous ses sièges"""
    connection = get_db_connection()
    
    if connection is None:
        return False, "Erreur de connexion à la base de données"
        
    try:
        cursor = connection.cursor()
        
        # Vérifier s'il y a des séances associées
        cursor.execute("SELECT COUNT(*) as count FROM showing WHERE room_id = %s", (room_id,))
        result = cursor.fetchone()
        if result and result[0] > 0:
            return False, "Impossible de supprimer cette salle car elle a des séances programmées"
        
        # Supprimer d'abord les sièges (à cause de la contrainte de clé étrangère)
        cursor.execute("DELETE FROM seat WHERE room_id = %s", (room_id,))
        
        # Puis supprimer la salle
        cursor.execute("DELETE FROM room WHERE id = %s", (room_id,))
        connection.commit()
        
        if cursor.rowcount > 0:
            return True, "Salle supprimée avec succès"
        else:
            return False, "Salle non trouvée"
        
    except Error as e:
        return False, f"Erreur lors de la suppression de la salle: {e}"
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# ===== FONCTIONS POUR LA GESTION DES SIÈGES =====

def update_seat_type(seat_id, new_type):
    """Met à jour le type d'un siège"""
    connection = get_db_connection()
    
    if connection is None:
        return False, "Erreur de connexion à la base de données"
        
    try:
        cursor = connection.cursor()
        
        cursor.execute("UPDATE seat SET type = %s WHERE id = %s", (new_type, seat_id))
        connection.commit()
        
        if cursor.rowcount > 0:
            return True, f"Type de siège mis à jour: {new_type}"
        else:
            return False, "Siège non trouvé"
        
    except Error as e:
        return False, f"Erreur lors de la mise à jour: {e}"
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_room_seats_grid(room_id):
    """Récupère tous les sièges d'une salle organisés en grille"""
    connection = get_db_connection()
    
    if connection is None:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Récupérer les informations de la salle
        cursor.execute("SELECT * FROM room WHERE id = %s", (room_id,))
        room = cursor.fetchone()
        
        if not room:
            return None
            
        # Récupérer tous les sièges de la salle
        cursor.execute("""
            SELECT id, seat_row, seat_column, type
            FROM seat 
            WHERE room_id = %s 
            ORDER BY seat_row, seat_column
        """, (room_id,))
        seats = cursor.fetchall()
        
        # Organiser en grille
        grid = {}
        for seat in seats:
            row = seat['seat_row']
            if row not in grid:
                grid[row] = {}
            grid[row][seat['seat_column']] = {
                'id': seat['id'],
                'type': seat['type']
            }
        
        return {
            'room': room,
            'grid': grid
        }
        
    except Error as e:
        print(f"Erreur lors de la récupération de la grille: {e}")
        return None
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_seat_by_position(room_id, seat_row, seat_column):
    """Récupère un siège par sa position"""
    connection = get_db_connection()
    
    if connection is None:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM seat 
            WHERE room_id = %s AND seat_row = %s AND seat_column = %s
        """, (room_id, seat_row, seat_column))
        
        return cursor.fetchone()
        
    except Error as e:
        print(f"Erreur lors de la récupération du siège: {e}")
        return None
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# ===== FONCTIONS POUR LES SÉANCES =====

def get_all_showings():
    """Récupère toutes les séances avec les informations des films et salles"""
    connection = get_db_connection()
    
    if connection is None:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.*, m.name as movie_name, m.duration, r.name as room_name
            FROM showing s
            JOIN movie m ON s.movie_id = m.id
            JOIN room r ON s.room_id = r.id
            ORDER BY s.date, s.starttime
        """)
        showings = cursor.fetchall()
        return showings
        
    except Error as e:
        print(f"Erreur lors de la récupération des séances: {e}")
        return None
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_showings_today():
    """Récupère les séances d'aujourd'hui"""
    connection = get_db_connection()
    
    if connection is None:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("""
            SELECT s.*, m.name as movie_name, m.duration, r.name as room_name
            FROM showing s
            JOIN movie m ON s.movie_id = m.id
            JOIN room r ON s.room_id = r.id
            WHERE DATE(s.date) = %s
            ORDER BY s.starttime
        """, (today,))
        showings = cursor.fetchall()
        return showings
        
    except Error as e:
        print(f"Erreur lors de la récupération des séances: {e}")
        return None
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_showings_by_movie(movie_id):
    """Récupère toutes les séances d'un film spécifique"""
    connection = get_db_connection()
    
    if connection is None:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.*, m.name as movie_name, m.duration, r.name as room_name
            FROM showing s
            JOIN movie m ON s.movie_id = m.id
            JOIN room r ON s.room_id = r.id
            WHERE s.movie_id = %s
            ORDER BY s.date, s.starttime
        """, (movie_id,))
        showings = cursor.fetchall()
        return showings
        
    except Error as e:
        print(f"Erreur lors de la récupération des séances: {e}")
        return None
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def add_showing(date, starttime, baseprice, room_id, movie_id):
    """Ajoute une nouvelle séance"""
    connection = get_db_connection()
    
    if connection is None:
        return False, "Erreur de connexion à la base de données"
        
    try:
        cursor = connection.cursor()
        
        cursor.execute("""
            INSERT INTO showing (date, starttime, baseprice, room_id, movie_id) 
            VALUES (%s, %s, %s, %s, %s)
        """, (date, starttime, baseprice, room_id, movie_id))
        connection.commit()
        
        return True, "Séance ajoutée avec succès"
        
    except Error as e:
        return False, f"Erreur lors de l'ajout de la séance: {e}"
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def update_showing(showing_id, date, starttime, baseprice, room_id, movie_id):
    """Met à jour une séance"""
    connection = get_db_connection()
    
    if connection is None:
        return False, "Erreur de connexion à la base de données"
        
    try:
        cursor = connection.cursor()
        
        cursor.execute("""
            UPDATE showing 
            SET date = %s, starttime = %s, baseprice = %s, room_id = %s, movie_id = %s
            WHERE id = %s
        """, (date, starttime, baseprice, room_id, movie_id, showing_id))
        connection.commit()
        
        if cursor.rowcount > 0:
            return True, "Séance mise à jour avec succès"
        else:
            return False, "Séance non trouvée"
        
    except Error as e:
        return False, f"Erreur lors de la mise à jour de la séance: {e}"
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def delete_showing(showing_id):
    """Supprime une séance"""
    connection = get_db_connection()
    
    if connection is None:
        return False, "Erreur de connexion à la base de données"
        
    try:
        cursor = connection.cursor()
        
        # Vérifier s'il y a des réservations associées
        cursor.execute("SELECT COUNT(*) as count FROM seatreservation WHERE showing_id = %s", (showing_id,))
        result = cursor.fetchone()
        if result and result[0] > 0:
            return False, "Impossible de supprimer cette séance car elle a des réservations"
        
        cursor.execute("DELETE FROM showing WHERE id = %s", (showing_id,))
        connection.commit()
        
        if cursor.rowcount > 0:
            return True, "Séance supprimée avec succès"
        else:
            return False, "Séance non trouvée"
        
    except Error as e:
        return False, f"Erreur lors de la suppression de la séance: {e}"
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# ===== FONCTIONS UTILITAIRES =====

def get_room_layout(room_id):
    """Récupère la disposition des sièges d'une salle"""
    connection = get_db_connection()
    
    if connection is None:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT seat_row, seat_column, type
            FROM seat 
            WHERE room_id = %s 
            ORDER BY seat_row, seat_column
        """, (room_id,))
        seats = cursor.fetchall()
        
        if not seats:
            return None
            
        # Organiser les sièges par rangée
        layout = {}
        for seat in seats:
            row = seat['seat_row']
            if row not in layout:
                layout[row] = []
            layout[row].append({
                'number': seat['seat_column'],
                'type': seat['type']
            })
        
        return layout
        
    except Error as e:
        print(f"Erreur lors de la récupération de la disposition: {e}")
        return None
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def print_room_layout(room_id):
    """Affiche la disposition des sièges d'une salle de manière visuelle"""
    layout = get_room_layout(room_id)
    
    if not layout:
        print(f"Aucun siège trouvé pour la salle {room_id}")
        return
    
    print(f"\n=== Disposition de la salle {room_id} ===")
    print("ÉCRAN")
    print("-" * 40)
    
    for row_letter in sorted(layout.keys()):
        row_seats = layout[row_letter]
        row_display = f"{row_letter} |"
        
        for seat in sorted(row_seats, key=lambda x: x['number']):
            # Choisir le symbole selon le type de siège
            if seat['type'] == 'pmr':
                seat_symbol = "♿"
            elif seat['type'] == 'stair':
                seat_symbol = "🚪"
            elif seat['type'] == 'empty':
                seat_symbol = "  "
            else:  # normal
                seat_symbol = "💺"
            
            row_display += f" {seat_symbol}{seat['number']:2d}"
        
        print(row_display)
    
    print("-" * 40)
    print("Légende: 💺 = Normal, ♿ = PMR, 🚪 = Escalier,    = Vide")
