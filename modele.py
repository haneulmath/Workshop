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
    """Met à jour une salle - permet de changer les dimensions seulement si la salle n'est pas utilisée"""
    connection = get_db_connection()
    
    if connection is None:
        return False, "Erreur de connexion à la base de données"
        
    try:
        cursor = connection.cursor()
        
        # Récupérer les dimensions actuelles de la salle
        cursor.execute("SELECT name, nb_rows, nb_columns FROM room WHERE id = %s", (room_id,))
        current_room = cursor.fetchone()
        
        if not current_room:
            return False, "Salle non trouvée"
        
        current_name, current_rows, current_columns = current_room
        
        # Vérifier si les dimensions changent
        dimensions_changed = (nb_rows != current_rows or nb_columns != current_columns)
        
        if dimensions_changed:
            # Vérifier si la salle est utilisée dans des séances
            if is_room_used_in_showings(room_id):
                return False, "Impossible de modifier les dimensions de cette salle car elle est utilisée dans des séances. Supprimez d'abord toutes les séances associées."
            
            # Si les dimensions changent, il faut recréer tous les sièges
            # Supprimer tous les sièges existants
            cursor.execute("DELETE FROM seat WHERE room_id = %s", (room_id,))
            
            # Mettre à jour la salle avec les nouvelles dimensions
            cursor.execute("UPDATE room SET name = %s, nb_rows = %s, nb_columns = %s WHERE id = %s", 
                         (name, nb_rows, nb_columns, room_id))
            
            # Recréer les sièges avec les nouvelles dimensions
            seats_created = 0
            for row_num in range(1, nb_rows + 1):
                row_letter = chr(ord('A') + row_num - 1)
                for seat_column in range(1, nb_columns + 1):
                    cursor.execute("""
                        INSERT INTO seat (type, room_id, seat_row, seat_column) 
                        VALUES ('normal', %s, %s, %s)
                    """, (room_id, row_letter, seat_column))
                    seats_created += 1
            
            connection.commit()
            return True, f"Salle '{name}' mise à jour avec succès (dimensions changées: {seats_created} sièges recréés)"
        else:
            # Seul le nom change, mise à jour simple
            cursor.execute("UPDATE room SET name = %s WHERE id = %s", (name, room_id))
            connection.commit()
            
            if cursor.rowcount > 0:
                return True, f"Salle '{name}' mise à jour avec succès"
            else:
                return False, "Aucune modification effectuée"
        
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
        
        # Vérifier si la salle contenant ce siège a des séances avec des réservations
        if has_room_bookings_for_seat(seat_id):
            return False, "Impossible de modifier le type de siège : la salle a des séances avec des réservations"
        
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

def get_seat_by_id(seat_id):
    """Récupère les informations d'un siège par son ID"""
    connection = get_db_connection()
    
    if connection is None:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.id, s.seat_row, s.seat_column, s.type, r.name as room_name
            FROM seat s
            JOIN room r ON s.room_id = r.id
            WHERE s.id = %s
        """, (seat_id,))
        
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

def get_showing_by_id(showing_id):
    """Récupère une séance par son ID avec les informations du film et de la salle"""
    connection = get_db_connection()
    
    if connection is None:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.*, m.name as movie, m.duration, r.name as room, r.id as room_id
            FROM showing s
            JOIN movie m ON s.movie_id = m.id
            JOIN room r ON s.room_id = r.id
            WHERE s.id = %s
        """, (showing_id,))
        showing = cursor.fetchone()
        
        if showing:
            # Convertir le prix de centimes en euros
            showing['price'] = showing['baseprice'] / 100
            # S'assurer que time est un objet time
            if isinstance(showing['starttime'], str):
                showing['time'] = showing['starttime']
            else:
                showing['time'] = str(showing['starttime'])
        
        return showing
        
    except Error as e:
        print(f"Erreur lors de la récupération de la séance: {e}")
        return None
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_showing_info(showing_id):
    """Récupère les informations d'une séance avec les détails de la salle"""
    connection = get_db_connection()
    
    if connection is None:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.*, r.name as room_name, r.nb_rows, r.nb_columns, m.name as movie_name
            FROM showing s
            JOIN room r ON s.room_id = r.id
            JOIN movie m ON s.movie_id = m.id
            WHERE s.id = %s
        """, (showing_id,))
        showing_info = cursor.fetchone()
        return showing_info
        
    except Error as e:
        print(f"Erreur lors de la récupération des informations de séance: {e}")
        return None
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_showing_seats_grid(showing_id):
    """Récupère la grille de sièges pour une séance donnée"""
    connection = get_db_connection()
    
    if connection is None:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Récupérer les informations de la salle
        cursor.execute("""
            SELECT r.* FROM room r
            JOIN showing s ON r.id = s.room_id
            WHERE s.id = %s
        """, (showing_id,))
        room = cursor.fetchone()
        
        if not room:
            return None
        
        # Récupérer tous les sièges de la salle avec leur statut pour cette séance
        cursor.execute("""
            SELECT 
                s.id, s.type, s.seat_row, s.seat_column,
                CASE 
                    WHEN sr.seat_id IS NOT NULL THEN 'occupied'
                    ELSE 'available'
                END as status
            FROM seat s
            LEFT JOIN seatreservation sr ON s.id = sr.seat_id AND sr.showing_id = %s
            WHERE s.room_id = %s
            ORDER BY s.seat_row, s.seat_column
        """, (showing_id, room['id']))
        seats = cursor.fetchall()
        
        # Créer la grille
        grid = []
        for row_num in range(1, room['nb_rows'] + 1):
            row_letter = chr(64 + row_num)  # A, B, C, etc.
            grid_row = []
            for col in range(1, room['nb_columns'] + 1):
                # Trouver le siège correspondant
                seat = next((seat for seat in seats 
                           if seat['seat_row'] == row_letter and seat['seat_column'] == col), None)
                grid_row.append(seat)
            grid.append(grid_row)
        
        return {
            'room': room,
            'grid': grid
        }
        
    except Error as e:
        print(f"Erreur lors de la récupération de la grille de sièges: {e}")
        return None
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def book_seats(showing_id, seat_ids, user_id):
    """Effectue une réservation pour les sièges sélectionnés"""
    connection = get_db_connection()
    
    if connection is None:
        return False, "Erreur de connexion à la base de données"
        
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Vérifier que tous les sièges sont disponibles
        seat_ids_str = ','.join(map(str, seat_ids))
        cursor.execute(f"""
            SELECT s.id, s.seat_row, s.seat_column, s.type,
                   se.baseprice, m.name as movie, r.name as room, se.date, se.starttime
            FROM seat s
            JOIN room r ON s.room_id = r.id
            JOIN showing se ON r.id = se.room_id
            JOIN movie m ON se.movie_id = m.id
            LEFT JOIN seatreservation sr ON s.id = sr.seat_id AND sr.showing_id = %s
            WHERE s.id IN ({seat_ids_str}) AND se.id = %s AND sr.seat_id IS NULL
        """, (showing_id, showing_id))
        
        available_seats = cursor.fetchall()
        
        if len(available_seats) != len(seat_ids):
            return False, "Certains sièges ne sont plus disponibles"
        
        # Calculer le prix total
        price_per_seat = available_seats[0]['baseprice'] / 100
        total_price = price_per_seat * len(seat_ids)
        
        # Créer la réservation principale
        cursor.execute("""
            INSERT INTO booking (price, account_id, showing_id) 
            VALUES (%s, %s, %s)
        """, (total_price, user_id, showing_id))
        booking_id = cursor.lastrowid
        
        # Créer les clients et réservations de sièges
        for i, seat in enumerate(available_seats):
            # Créer un client fictif pour chaque siège (en production, vous devriez demander ces infos)
            cursor.execute("""
                INSERT INTO customer (firstname, lastname, age, pmr, booking_id) 
                VALUES (%s, %s, %s, %s, %s)
            """, (f"Client{i+1}", "Nom", 25, 0, booking_id))
            customer_id = cursor.lastrowid
            
            # Créer la réservation de siège
            cursor.execute("""
                INSERT INTO seatreservation (customer_id, showing_id, seat_id) 
                VALUES (%s, %s, %s)
            """, (customer_id, showing_id, seat['id']))
        
        connection.commit()
        
        # Préparer les données de retour
        booking_data = {
            'movie': available_seats[0]['movie'],
            'room': available_seats[0]['room'],
            'date': available_seats[0]['date'],
            'time': str(available_seats[0]['starttime']),
            'seats': [{'row': seat['seat_row'], 'col': seat['seat_column'], 'type': seat['type']} 
                     for seat in available_seats],
            'price_per_seat': price_per_seat,
            'total_price': total_price
        }
        
        return True, {
            'booking_id': booking_id,
            'booking': booking_data
        }
        
    except Error as e:
        print(f"Erreur lors de la réservation: {e}")
        return False, f"Erreur lors de la réservation: {e}"
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def book_seats_with_spectators(showing_id, seat_ids, spectators_data, user_id, total_price):
    """Effectue une réservation avec les informations détaillées des spectateurs"""
    connection = get_db_connection()
    
    if connection is None:
        return False, "Erreur de connexion à la base de données"
        
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Vérifier que tous les sièges sont disponibles
        seat_ids_str = ','.join(map(str, seat_ids))
        cursor.execute(f"""
            SELECT s.id, s.seat_row, s.seat_column, s.type
            FROM seat s
            LEFT JOIN seatreservation sr ON s.id = sr.seat_id AND sr.showing_id = %s
            WHERE s.id IN ({seat_ids_str}) AND sr.seat_id IS NULL
        """, (showing_id,))
        
        available_seats = cursor.fetchall()
        
        if len(available_seats) != len(seat_ids):
            return False, "Certains sièges ne sont plus disponibles"
        
        # Créer la réservation principale
        cursor.execute("""
            INSERT INTO booking (price, account_id, showing_id) 
            VALUES (%s, %s, %s)
        """, (total_price, user_id, showing_id))
        booking_id = cursor.lastrowid
        
        # Créer les clients et réservations de sièges avec les vraies informations
        for i, seat_id in enumerate(seat_ids):
            if i in spectators_data:
                spectator = spectators_data[i]
                first_name = spectator.get('first_name', f'Client{i+1}')
                last_name = spectator.get('last_name', 'Nom')
                age = int(spectator.get('age', 25))
                
                # Déterminer si c'est une place PMR
                seat_info = next((s for s in available_seats if s['id'] == seat_id), None)
                is_pmr = seat_info and seat_info['type'] == 'pmr'
                
                # Créer le client avec les vraies informations
                cursor.execute("""
                    INSERT INTO customer (firstname, lastname, age, pmr, booking_id) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (first_name, last_name, age, 1 if is_pmr else 0, booking_id))
                customer_id = cursor.lastrowid
                
                # Créer la réservation de siège
                cursor.execute("""
                    INSERT INTO seatreservation (customer_id, showing_id, seat_id) 
                    VALUES (%s, %s, %s)
                """, (customer_id, showing_id, seat_id))
        
        connection.commit()
        
        # Récupérer les informations de la séance pour la confirmation
        showing = get_showing_by_id(showing_id)
        
        # Préparer les données de retour
        booking_data = {
            'movie': showing['movie'] if showing else 'Film inconnu',
            'room': showing['room'] if showing else 'Salle inconnue',
            'date': showing['date'] if showing else None,
            'time': showing['time'] if showing else None,
            'seats': [{'id': seat['id'], 'row': seat['seat_row'], 'col': seat['seat_column'], 'type': seat['type']} 
                     for seat in available_seats],
            'total_price': total_price
        }
        
        return True, {
            'booking_id': booking_id,
            'booking': booking_data
        }
        
    except Error as e:
        print(f"Erreur lors de la réservation avec spectateurs: {e}")
        return False, f"Erreur lors de la réservation: {e}"
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_user_bookings(user_id):
    """Récupère toutes les réservations d'un utilisateur avec les détails"""
    connection = get_db_connection()
    
    if connection is None:
        return []
        
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Récupérer les réservations avec les détails des séances et films
        cursor.execute("""
            SELECT b.id as booking_id, b.price,
                   s.id as showing_id, s.date, s.starttime,
                   m.name as movie_name, m.duration,
                   r.name as room_name,
                   COUNT(sr.seat_id) as seat_count
            FROM booking b
            JOIN showing s ON b.showing_id = s.id
            JOIN movie m ON s.movie_id = m.id
            JOIN room r ON s.room_id = r.id
            JOIN seatreservation sr ON sr.showing_id = s.id
            JOIN customer c ON sr.customer_id = c.id AND c.booking_id = b.id
            WHERE b.account_id = %s
            GROUP BY b.id, s.id, m.id, r.id
            ORDER BY b.id DESC
        """, (user_id,))
        
        bookings = cursor.fetchall()
        
        # Pour chaque réservation, récupérer les détails des places et spectateurs
        for booking in bookings:
            # Le prix est déjà en euros dans la base selon le schéma V4.sql
            booking['price_euros'] = float(booking['price']) if booking['price'] else 0.0
            booking['time'] = str(booking['starttime'])
            
            # Récupérer les détails des places et spectateurs
            cursor.execute("""
                SELECT c.firstname, c.lastname, c.age, c.pmr,
                       st.seat_row, st.seat_column, st.type as seat_type
                FROM customer c
                JOIN seatreservation sr ON c.id = sr.customer_id
                JOIN seat st ON sr.seat_id = st.id
                WHERE c.booking_id = %s AND sr.showing_id = %s
                ORDER BY st.seat_row, st.seat_column
            """, (booking['booking_id'], booking['showing_id']))
            
            booking['seats_details'] = cursor.fetchall()
        
        return bookings
        
    except Error as e:
        print(f"Erreur lors de la récupération des réservations: {e}")
        return []
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_booking_details(booking_id, user_id):
    """Récupère les détails complets d'une réservation spécifique"""
    connection = get_db_connection()
    
    if connection is None:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Vérifier que la réservation appartient à l'utilisateur
        cursor.execute("""
            SELECT b.id as booking_id, b.price,
                   s.id as showing_id, s.date, s.starttime,
                   m.name as movie_name, m.duration, m.director, m.cast,
                   r.name as room_name
            FROM booking b
            JOIN showing s ON b.showing_id = s.id
            JOIN movie m ON s.movie_id = m.id
            JOIN room r ON s.room_id = r.id
            WHERE b.id = %s AND b.account_id = %s
        """, (booking_id, user_id))
        
        booking = cursor.fetchone()
        
        if not booking:
            return None
        
        booking['price_euros'] = float(booking['price']) if booking['price'] else 0.0
        booking['time'] = str(booking['starttime'])
        
        # Récupérer les détails des places et spectateurs
        cursor.execute("""
            SELECT c.firstname, c.lastname, c.age, c.pmr,
                   st.seat_row, st.seat_column, st.type as seat_type,
                   st.id as seat_id
            FROM customer c
            JOIN seatreservation sr ON c.id = sr.customer_id
            JOIN seat st ON sr.seat_id = st.id
            WHERE c.booking_id = %s AND sr.showing_id = %s
            ORDER BY st.seat_row, st.seat_column
        """, (booking['booking_id'], booking['showing_id']))
        
        booking['seats_details'] = cursor.fetchall()
        
        return booking
        
    except Error as e:
        print(f"Erreur lors de la récupération des détails de réservation: {e}")
        return None
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_all_bookings():
    """Récupère toutes les réservations pour l'administration"""
    connection = get_db_connection()
    
    if connection is None:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT b.id as booking_id, b.price,
                   s.id as showing_id, s.date, s.starttime,
                   m.name as movie_name,
                   r.name as room_name,
                   a.username, a.email,
                   COUNT(sr.seat_id) as seat_count,
                   GROUP_CONCAT(CONCAT(st.seat_row, st.seat_column) ORDER BY st.seat_row, st.seat_column) as seats
            FROM booking b
            JOIN showing s ON b.showing_id = s.id
            JOIN movie m ON s.movie_id = m.id
            JOIN room r ON s.room_id = r.id
            JOIN account a ON b.account_id = a.id
            JOIN seatreservation sr ON sr.showing_id = s.id
            JOIN customer c ON sr.customer_id = c.id AND c.booking_id = b.id
            JOIN seat st ON sr.seat_id = st.id
            GROUP BY b.id, s.id, m.id, r.id, a.id
            ORDER BY b.id DESC
        """)
        
        bookings = cursor.fetchall()
        
        # Convertir le prix et formater les données
        for booking in bookings:
            booking['price_euros'] = float(booking['price']) if booking['price'] else 0.0
            booking['time'] = str(booking['starttime'])
            # Convertir la liste de places en array
            if booking['seats']:
                booking['seats_list'] = booking['seats'].split(',')
            else:
                booking['seats_list'] = []
        
        return bookings
        
    except Error as e:
        print(f"Erreur lors de la récupération des réservations: {e}")
        return None
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def cancel_booking(booking_id):
    """Annule une réservation (supprime toutes les données associées)"""
    connection = get_db_connection()
    
    if connection is None:
        return False, "Erreur de connexion à la base de données"
        
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Vérifier que la réservation existe
        cursor.execute("SELECT id FROM booking WHERE id = %s", (booking_id,))
        booking = cursor.fetchone()
        
        if not booking:
            return False, "Réservation non trouvée"
        
        # Supprimer les réservations de sièges (cela libère les sièges)
        cursor.execute("""
            DELETE sr FROM seatreservation sr 
            JOIN customer c ON sr.customer_id = c.id 
            WHERE c.booking_id = %s
        """, (booking_id,))
        
        # Supprimer les clients
        cursor.execute("DELETE FROM customer WHERE booking_id = %s", (booking_id,))
        
        # Supprimer la réservation principale
        cursor.execute("DELETE FROM booking WHERE id = %s", (booking_id,))
        
        connection.commit()
        
        return True, "Réservation annulée avec succès"
        
    except Error as e:
        print(f"Erreur lors de l'annulation de la réservation: {e}")
        return False, f"Erreur lors de l'annulation: {e}"
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def add_showing(date, starttime, baseprice, room_id, movie_id):
    """Ajouter une nouvelle séance"""
    connection = get_db_connection()
    
    if connection is None:
        return False, "Erreur de connexion à la base de données"
    
    try:
        cursor = connection.cursor()
        
        # Vérifier que le film existe
        cursor.execute("SELECT id FROM movie WHERE id = %s", (movie_id,))
        if not cursor.fetchone():
            return False, "Film non trouvé"
        
        # Vérifier que la salle existe
        cursor.execute("SELECT id FROM room WHERE id = %s", (room_id,))
        if not cursor.fetchone():
            return False, "Salle non trouvée"
        
        # Vérifier qu'il n'y a pas de conflit d'horaire dans la même salle
        cursor.execute("""
            SELECT id FROM showing 
            WHERE room_id = %s AND date = %s AND starttime = %s
        """, (room_id, date, starttime))
        
        if cursor.fetchone():
            return False, "Une séance existe déjà à cette heure dans cette salle"
        
        # Ajouter la séance
        cursor.execute("""
            INSERT INTO showing (date, starttime, baseprice, room_id, movie_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (date, starttime, baseprice, room_id, movie_id))
        
        connection.commit()
        return True, "Séance ajoutée avec succès"
        
    except Error as e:
        print(f"Erreur lors de l'ajout de la séance: {e}")
        return False, f"Erreur lors de l'ajout: {e}"
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def update_showing(showing_id, date, starttime, baseprice, room_id, movie_id):
    """Mettre à jour une séance"""
    connection = get_db_connection()
    
    if connection is None:
        return False, "Erreur de connexion à la base de données"
    
    try:
        cursor = connection.cursor()
        
        # Vérifier que la séance existe
        cursor.execute("SELECT id FROM showing WHERE id = %s", (showing_id,))
        if not cursor.fetchone():
            return False, "Séance non trouvée"
        
        # Vérifier que le film existe
        cursor.execute("SELECT id FROM movie WHERE id = %s", (movie_id,))
        if not cursor.fetchone():
            return False, "Film non trouvé"
        
        # Vérifier que la salle existe
        cursor.execute("SELECT id FROM room WHERE id = %s", (room_id,))
        if not cursor.fetchone():
            return False, "Salle non trouvée"
        
        # Vérifier qu'il n'y a pas de conflit d'horaire (en excluant la séance actuelle)
        cursor.execute("""
            SELECT id FROM showing 
            WHERE room_id = %s AND date = %s AND starttime = %s AND id != %s
        """, (room_id, date, starttime, showing_id))
        
        if cursor.fetchone():
            return False, "Une autre séance existe déjà à cette heure dans cette salle"
        
        # Mettre à jour la séance
        cursor.execute("""
            UPDATE showing 
            SET date = %s, starttime = %s, baseprice = %s, room_id = %s, movie_id = %s
            WHERE id = %s
        """, (date, starttime, baseprice, room_id, movie_id, showing_id))
        
        connection.commit()
        return True, "Séance mise à jour avec succès"
        
    except Error as e:
        print(f"Erreur lors de la mise à jour de la séance: {e}")
        return False, f"Erreur lors de la mise à jour: {e}"
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def delete_showing(showing_id):
    """Supprimer une séance"""
    connection = get_db_connection()
    
    if connection is None:
        return False, "Erreur de connexion à la base de données"
    
    try:
        cursor = connection.cursor()
        
        # Vérifier que la séance existe
        cursor.execute("SELECT id FROM showing WHERE id = %s", (showing_id,))
        if not cursor.fetchone():
            return False, "Séance non trouvée"
        
        # Vérifier s'il y a des réservations pour cette séance
        cursor.execute("SELECT COUNT(*) FROM booking WHERE showing_id = %s", (showing_id,))
        result = cursor.fetchone()
        if result and result[0] > 0:
            return False, "Impossible de supprimer une séance avec des réservations existantes"
        
        # Supprimer la séance
        cursor.execute("DELETE FROM showing WHERE id = %s", (showing_id,))
        
        connection.commit()
        return True, "Séance supprimée avec succès"
        
    except Error as e:
        print(f"Erreur lors de la suppression de la séance: {e}")
        return False, f"Erreur lors de la suppression: {e}"
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def is_room_used_in_showings(room_id):
    """Vérifie si une salle est utilisée dans des séances"""
    connection = get_db_connection()
    
    if connection is None:
        return True  # En cas d'erreur, on considère que la salle est utilisée pour éviter les suppressions
        
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM showing WHERE room_id = %s", (room_id,))
        count = cursor.fetchone()[0]
        return count > 0
        
    except Error as e:
        print(f"Erreur lors de la vérification de l'utilisation de la salle: {e}")
        return True  # En cas d'erreur, on considère que la salle est utilisée
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def has_room_bookings_for_seat(seat_id):
    """Vérifie si la salle contenant ce siège a des séances avec des réservations"""
    connection = get_db_connection()
    
    if connection is None:
        return True  # En cas d'erreur, on considère qu'il y a des réservations pour éviter les modifications
        
    try:
        cursor = connection.cursor()
        
        # Récupérer la salle du siège et vérifier s'il y a des réservations pour des séances dans cette salle
        query = """
        SELECT COUNT(*) 
        FROM booking b
        JOIN showing s ON b.showing_id = s.id
        JOIN seat st ON s.room_id = st.room_id
        WHERE st.id = %s
        """
        cursor.execute(query, (seat_id,))
        count = cursor.fetchone()[0]
        return count > 0
        
    except Error as e:
        print(f"Erreur lors de la vérification des réservations pour la salle: {e}")
        return True  # En cas d'erreur, on considère qu'il y a des réservations
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# ===== FONCTIONS POUR LES AFFICHES DE FILMS =====

def get_movie_poster(movie_id):
    """Récupère l'affiche principale d'un film"""
    connection = get_db_connection()
    
    if connection is None:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT image, name, mime_type, file_size
            FROM movieposter 
            WHERE movie_id = %s AND is_primary = TRUE
            LIMIT 1
        """, (movie_id,))
        
        poster = cursor.fetchone()
        return poster
        
    except Error as e:
        print(f"Erreur lors de la récupération de l'affiche: {e}")
        return None
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def save_movie_poster(movie_id, filename, mime_type, image_data):
    """Sauvegarde ou met à jour l'affiche d'un film"""
    connection = get_db_connection()
    
    if connection is None:
        return False, "Erreur de connexion à la base de données"
        
    try:
        cursor = connection.cursor()
        
        # Supprimer l'affiche existante s'il y en a une
        cursor.execute("DELETE FROM movieposter WHERE movie_id = %s", (movie_id,))
        
        # Insérer la nouvelle affiche
        file_size = len(image_data)
        cursor.execute("""
            INSERT INTO movieposter (movie_id, name, mime_type, image, file_size, is_primary)
            VALUES (%s, %s, %s, %s, %s, TRUE)
        """, (movie_id, filename, mime_type, image_data, file_size))
        
        connection.commit()
        return True, "Affiche téléchargée avec succès"
        
    except Error as e:
        print(f"Erreur lors de la sauvegarde de l'affiche: {e}")
        return False, f"Erreur lors de la sauvegarde: {str(e)}"
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def delete_movie_poster(movie_id):
    """Supprime l'affiche d'un film"""
    connection = get_db_connection()
    
    if connection is None:
        return False, "Erreur de connexion à la base de données"
        
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Vérifier s'il y a une affiche à supprimer
        cursor.execute("SELECT COUNT(*) as count FROM movieposter WHERE movie_id = %s", (movie_id,))
        result = cursor.fetchone()
        
        if result['count'] == 0:
            return False, "Aucune affiche à supprimer"
        
        # Supprimer l'affiche
        cursor.execute("DELETE FROM movieposter WHERE movie_id = %s", (movie_id,))
        connection.commit()
        
        return True, "Affiche supprimée avec succès"
        
    except Error as e:
        print(f"Erreur lors de la suppression de l'affiche: {e}")
        return False, f"Erreur lors de la suppression: {str(e)}"
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# ===== FONCTIONS D'ADMINISTRATION DES AFFICHES =====

def create_movieposter_table():
    """Crée la table movieposter si elle n'existe pas"""
    connection = get_db_connection()
    
    if connection is None:
        return False, "Erreur de connexion à la base de données"
        
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movieposter (
                id INT AUTO_INCREMENT PRIMARY KEY,
                movie_id INT NOT NULL,
                image LONGBLOB NOT NULL,
                name VARCHAR(255) NOT NULL,
                mime_type VARCHAR(100) NOT NULL,
                file_size INT,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_primary BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (movie_id) REFERENCES movie(id) ON DELETE CASCADE,
                INDEX idx_movie_id (movie_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        connection.commit()
        return True, "Table movieposter créée avec succès"
        
    except Error as e:
        print(f"Erreur lors de la création de la table movieposter: {e}")
        return False, f"Erreur lors de la création: {str(e)}"
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def insert_poster_from_file(movie_id, file_path, filename=None):
    """Insère une affiche depuis un fichier local"""
    import os
    import mimetypes
    
    if not os.path.exists(file_path):
        return False, f"Fichier non trouvé: {file_path}"
    
    if filename is None:
        filename = os.path.basename(file_path)
    
    # Déterminer le type MIME
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'
    
    try:
        # Lire le fichier
        with open(file_path, 'rb') as f:
            image_data = f.read()
        
        # Utiliser la fonction existante save_movie_poster
        return save_movie_poster(movie_id, filename, mime_type, image_data)
        
    except Exception as e:
        return False, f"Erreur lors de la lecture du fichier: {str(e)}"

def list_movie_posters():
    """Liste toutes les affiches dans la base de données"""
    connection = get_db_connection()
    
    if connection is None:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                mp.id,
                mp.movie_id,
                m.name as movie_name,
                mp.name as poster_name,
                mp.mime_type,
                mp.file_size,
                mp.upload_date,
                mp.is_primary
            FROM movieposter mp
            JOIN movie m ON mp.movie_id = m.id
            ORDER BY m.name
        """)
        
        posters = cursor.fetchall()
        return posters
        
    except Error as e:
        print(f"Erreur lors de la récupération des affiches: {e}")
        return None
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
