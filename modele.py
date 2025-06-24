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

def add_movie(name, duration):
    """Ajoute un nouveau film"""
    connection = get_db_connection()
    
    if connection is None:
        return False, "Erreur de connexion à la base de données"
        
    try:
        cursor = connection.cursor()
        
        cursor.execute("INSERT INTO movie (name, duration) VALUES (%s, %s)", 
                      (name, duration))
        connection.commit()
        
        return True, f"Film '{name}' ajouté avec succès"
        
    except Error as e:
        return False, f"Erreur lors de l'ajout du film: {e}"
        
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

def get_all_seances():
    """Récupère toutes les séances avec les informations des films et salles"""
    connection = get_db_connection()
    
    if connection is None:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.*, m.name as movie_name, m.duration, r.name as room_name
            FROM seance s
            JOIN movie m ON s.movie_id = m.id
            JOIN room r ON s.room_id = r.id
            ORDER BY s.date, s.starttime
        """)
        seances = cursor.fetchall()
        return seances
        
    except Error as e:
        print(f"Erreur lors de la récupération des séances: {e}")
        return None
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_seances_today():
    """Récupère les séances d'aujourd'hui"""
    connection = get_db_connection()
    
    if connection is None:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("""
            SELECT s.*, m.name as movie_name, m.duration, r.name as room_name
            FROM seance s
            JOIN movie m ON s.movie_id = m.id
            JOIN room r ON s.room_id = r.id
            WHERE DATE(s.date) = %s
            ORDER BY s.starttime
        """, (today,))
        seances = cursor.fetchall()
        return seances
        
    except Error as e:
        print(f"Erreur lors de la récupération des séances: {e}")
        return None
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_seances_by_movie(movie_id):
    """Récupère toutes les séances d'un film spécifique"""
    connection = get_db_connection()
    
    if connection is None:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.*, m.name as movie_name, m.duration, r.name as room_name
            FROM seance s
            JOIN movie m ON s.movie_id = m.id
            JOIN room r ON s.room_id = r.id
            WHERE s.movie_id = %s
            ORDER BY s.date, s.starttime
        """, (movie_id,))
        seances = cursor.fetchall()
        return seances
        
    except Error as e:
        print(f"Erreur lors de la récupération des séances: {e}")
        return None
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def add_seance(date, starttime, baseprice, room_id, movie_id):
    """Ajoute une nouvelle séance"""
    connection = get_db_connection()
    
    if connection is None:
        return False, "Erreur de connexion à la base de données"
        
    try:
        cursor = connection.cursor()
        
        cursor.execute("""
            INSERT INTO seance (date, starttime, baseprice, room_id, movie_id) 
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

def get_seance_info(seance_id):
    """Récupère les informations d'une séance avec les détails de la salle"""
    connection = get_db_connection()
    
    if connection is None:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.*, r.name as room_name, r.nb_rows, r.nb_columns, m.name as movie_name
            FROM seance s
            JOIN room r ON s.room_id = r.id
            JOIN movie m ON s.movie_id = m.id
            WHERE s.id = %s
        """, (seance_id,))
        seance_info = cursor.fetchone()
        return seance_info
        
    except Error as e:
        print(f"Erreur lors de la récupération des informations de séance: {e}")
        return None
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_seance_by_id(seance_id):
    """Récupère une séance par son ID avec les informations du film et de la salle"""
    connection = get_db_connection()
    
    if connection is None:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.*, m.name as movie, m.duration, r.name as room, r.id as room_id
            FROM seance s
            JOIN movie m ON s.movie_id = m.id
            JOIN room r ON s.room_id = r.id
            WHERE s.id = %s
        """, (seance_id,))
        seance = cursor.fetchone()
        
        if seance:
            # Convertir le prix de centimes en euros
            seance['price'] = seance['baseprice'] / 100
            # S'assurer que time est un objet time
            if isinstance(seance['starttime'], str):
                seance['time'] = seance['starttime']
            else:
                seance['time'] = str(seance['starttime'])
        
        return seance
        
    except Error as e:
        print(f"Erreur lors de la récupération de la séance: {e}")
        return None
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_seance_seats_grid(seance_id):
    """Récupère la grille de sièges pour une séance donnée"""
    connection = get_db_connection()
    
    if connection is None:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Récupérer les informations de la salle
        cursor.execute("""
            SELECT r.* FROM room r
            JOIN seance s ON r.id = s.room_id
            WHERE s.id = %s
        """, (seance_id,))
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
            LEFT JOIN seatreservation sr ON s.id = sr.seat_id AND sr.seance_id = %s
            WHERE s.room_id = %s
            ORDER BY s.seat_row, s.seat_column
        """, (seance_id, room['id']))
        seats = cursor.fetchall()
        
        # Créer la grille
        grid = []
        for row in range(1, room['nb_rows'] + 1):
            grid_row = []
            for col in range(1, room['nb_columns'] + 1):
                # Trouver le siège correspondant
                seat = next((seat for seat in seats 
                           if seat['seat_row'] == row and seat['seat_column'] == col), None)
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

def book_seats(seance_id, seat_ids, user_id):
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
            JOIN seance se ON r.id = se.room_id
            JOIN movie m ON se.movie_id = m.id
            LEFT JOIN seatreservation sr ON s.id = sr.seat_id AND sr.seance_id = %s
            WHERE s.id IN ({seat_ids_str}) AND se.id = %s AND sr.seat_id IS NULL
        """, (seance_id, seance_id))
        
        available_seats = cursor.fetchall()
        
        if len(available_seats) != len(seat_ids):
            return False, "Certains sièges ne sont plus disponibles"
        
        # Calculer le prix total
        price_per_seat = available_seats[0]['baseprice'] / 100
        total_price = price_per_seat * len(seat_ids)
        
        # Créer la réservation principale
        cursor.execute("""
            INSERT INTO booking (price, account_id, seance_id) 
            VALUES (%s, %s, %s)
        """, (int(total_price * 100), user_id, seance_id))
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
                INSERT INTO seatreservation (customer_id, seance_id, seat_id) 
                VALUES (%s, %s, %s)
            """, (customer_id, seance_id, seat['id']))
        
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
