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
        """, (int(total_price * 100), user_id, showing_id))
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
        """, (int(total_price * 100), user_id, showing_id))
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
