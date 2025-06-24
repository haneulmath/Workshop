#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import mysql.connector
from mysql.connector import Error
import hashlib
from datetime import datetime, time

# Connexion à la BDD
DB_CONFIG = {
    "host": "82.66.24.184",
    "port":3305,
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

def initialize_database():
    """Initialise la base de données cinéma"""
    connection = get_db_connection()
    
    if connection:
        try:
            cursor = connection.cursor()
            
            # Créer la base de données si elle n'existe pas
            cursor.execute("CREATE DATABASE IF NOT EXISTS Cinemacousas")
            cursor.execute("USE Cinemacousas")
            
            # Vérifier si les tables existent déjà
            cursor.execute("SHOW TABLES")
            existing_tables = [table[0] for table in cursor.fetchall()]
            
            if len(existing_tables) == 0:
                # Créer les tables manuellement
                create_tables(cursor, connection)
                # Insérer des données de test
                insert_test_data(cursor, connection)
                print("Base de données initialisée avec succès")
            else:
                # Vérifier si la structure de la table room est correcte
                cursor.execute("DESCRIBE room")
                room_columns = [column[0] for column in cursor.fetchall()]
                
                if 'nb_rows' not in room_columns or 'capacity' in room_columns:
                    print("Structure de base de données obsolète détectée. Mise à jour...")
                    # Supprimer les tables dans le bon ordre (contraintes de clés étrangères)
                    drop_tables = [
                        "DROP TABLE IF EXISTS seatreservation",
                        "DROP TABLE IF EXISTS customer", 
                        "DROP TABLE IF EXISTS booking",
                        "DROP TABLE IF EXISTS seat",
                        "DROP TABLE IF EXISTS seance",
                        "DROP TABLE IF EXISTS movie",
                        "DROP TABLE IF EXISTS room",
                        "DROP TABLE IF EXISTS account",
                        "DROP TABLE IF EXISTS ageprice"
                    ]
                    
                    for drop_cmd in drop_tables:
                        cursor.execute(drop_cmd)
                    
                    # Recréer les tables avec la nouvelle structure
                    create_tables(cursor, connection)
                    insert_test_data(cursor, connection)
                    print("Base de données mise à jour avec succès")
                else:
                    print("Base de données déjà initialisée")
            
            return True
                
        except Error as e:
            print(f"Erreur lors de l'initialisation de la base de données: {e}")
            return False
        
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    return False

def create_tables(cursor, connection):
    """Crée les tables de la base de données"""
    
    # Table account
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS account (
            id INT NOT NULL AUTO_INCREMENT,
            email VARCHAR(100) NOT NULL,
            password_hash VARCHAR(100) NOT NULL,
            PRIMARY KEY (id),
            UNIQUE KEY email_UNIQUE (email)
        ) ENGINE = InnoDB
    """)
    
    # Table room
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS room (
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(45) NOT NULL,
            nb_rows INT NULL DEFAULT NULL,
            nb_columns INT NULL DEFAULT NULL,
            PRIMARY KEY (id)
        ) ENGINE = InnoDB
    """)
    
    # Table movie
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movie (
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(45) NOT NULL,
            duration INT NOT NULL,
            PRIMARY KEY (id)
        ) ENGINE = InnoDB
    """)
    
    # Table seance
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS seance (
            id INT NOT NULL AUTO_INCREMENT,
            date DATETIME NOT NULL,
            starttime TIME NOT NULL,
            baseprice INT NOT NULL,
            room_id INT NOT NULL,
            movie_id INT NOT NULL,
            PRIMARY KEY (id),
            KEY fk_seance_room1_idx (room_id),
            KEY fk_seance_movie1_idx (movie_id),
            CONSTRAINT fk_seance_room1 FOREIGN KEY (room_id) REFERENCES room (id) ON DELETE RESTRICT ON UPDATE CASCADE,
            CONSTRAINT fk_seance_movie1 FOREIGN KEY (movie_id) REFERENCES movie (id) ON DELETE RESTRICT ON UPDATE CASCADE
        ) ENGINE = InnoDB
    """)
    
    # Table booking
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS booking (
            id INT NOT NULL AUTO_INCREMENT,
            price DECIMAL(10,2) NULL DEFAULT NULL,
            account_id INT NOT NULL,
            seance_id INT NOT NULL,
            PRIMARY KEY (id),
            KEY fk_booking_account1_idx (account_id),
            KEY fk_booking_seance1_idx (seance_id),
            CONSTRAINT fk_booking_account1 FOREIGN KEY (account_id) REFERENCES account (id) ON DELETE RESTRICT ON UPDATE CASCADE,
            CONSTRAINT fk_booking_seance1 FOREIGN KEY (seance_id) REFERENCES seance (id) ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE = InnoDB
    """)
    
    # Table customer
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer (
            id INT NOT NULL AUTO_INCREMENT,
            firstname VARCHAR(45) NOT NULL,
            lastname VARCHAR(100) NOT NULL,
            age INT NOT NULL,
            pmr TINYINT NULL DEFAULT NULL,
            booking_id INT NOT NULL,
            PRIMARY KEY (id),
            KEY fk_customer_booking1_idx (booking_id),
            CONSTRAINT fk_customer_booking1 FOREIGN KEY (booking_id) REFERENCES booking (id) ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE = InnoDB
    """)
    
    # Table seat
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS seat (
            id INT NOT NULL AUTO_INCREMENT,
            type ENUM('normal', 'pmr', 'stair', 'empty') NULL DEFAULT 'normal',
            room_id INT NOT NULL,
            seat_row VARCHAR(45) NOT NULL,
            seat_column INT NOT NULL,
            PRIMARY KEY (id),
            UNIQUE KEY unique_seat_per_room (seat_row, seat_column, room_id),
            KEY fk_seat_room1_idx (room_id),
            CONSTRAINT fk_seat_room1 FOREIGN KEY (room_id) REFERENCES room (id) ON DELETE RESTRICT ON UPDATE CASCADE
        ) ENGINE = InnoDB
    """)
    
    # Table seatreservation
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS seatreservation (
            customer_id INT NOT NULL,
            seance_id INT NOT NULL,
            seat_id INT NOT NULL,
            PRIMARY KEY (seance_id, seat_id),
            KEY fk_seatreservation_customer1_idx (customer_id),
            KEY fk_seatreservation_seat1_idx (seat_id),
            CONSTRAINT fk_seatreservation_customer1 FOREIGN KEY (customer_id) REFERENCES customer (id) ON DELETE CASCADE ON UPDATE CASCADE,
            CONSTRAINT fk_seatreservation_seance1 FOREIGN KEY (seance_id) REFERENCES seance (id) ON DELETE RESTRICT ON UPDATE CASCADE,
            CONSTRAINT fk_seatreservation_seat1 FOREIGN KEY (seat_id) REFERENCES seat (id) ON DELETE RESTRICT ON UPDATE CASCADE
        ) ENGINE = InnoDB
    """)
    
    # Table ageprice
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ageprice (
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(45) NOT NULL,
            agemax INT NOT NULL,
            agemin INT NOT NULL,
            factor DECIMAL(4,2) NOT NULL,
            PRIMARY KEY (id)
        ) ENGINE = InnoDB
    """)
    
    connection.commit()

def insert_test_data(cursor, connection):
    """Insère des données de test dans la base de données"""
    try:
        # Vérifier si des données existent déjà
        cursor.execute("SELECT COUNT(*) FROM movie")
        if cursor.fetchone()[0] > 0:
            return  # Des données existent déjà
            
        # Insérer des comptes de test
        cursor.execute("""
            INSERT INTO account (email, password_hash) VALUES 
            ('admin@cinema.com', %s),
            ('user@cinema.com', %s)
        """, (hash_password('admin123'), hash_password('user123')))
        
        # Insérer des salles
        cursor.execute("""
            INSERT INTO room (name, nb_rows, nb_columns) VALUES 
            ('Salle 1', 6, 10),
            ('Salle 2', 8, 10),
            ('Salle VIP', 4, 10)
        """)
        
        # Insérer des films
        cursor.execute("""
            INSERT INTO movie (name, duration) VALUES 
            ('Dune: Part Two', 155),
            ('The Creator', 133),
            ('Oppenheimer', 180)
        """)
        
        # Insérer des sièges pour chaque salle
        for room_id in range(1, 4):
            nb_rows = 6 if room_id == 1 else (8 if room_id == 2 else 4)
            nb_columns = 10
            
            for row in range(1, nb_rows + 1):
                for seat_num in range(1, nb_columns + 1):
                    # Tous les sièges sont normaux par défaut
                    seat_type = 'normal'
                    seat_row = chr(64 + row)  # A, B, C, etc.
                    cursor.execute("""
                        INSERT INTO seat (type, room_id, seat_row, seat_column) 
                        VALUES (%s, %s, %s, %s)
                    """, (seat_type, room_id, seat_row, seat_num))
        
        # Insérer des séances (plusieurs dates et horaires)
        cursor.execute("""
            INSERT INTO seance (date, starttime, baseprice, room_id, movie_id) VALUES 
            ('2025-06-24', '18:00:00', 1200, 1, 1),
            ('2025-06-24', '20:00:00', 1200, 2, 2),
            ('2025-06-24', '22:00:00', 1500, 3, 3),
            ('2025-06-25', '18:00:00', 1200, 1, 2),
            ('2025-06-25', '20:00:00', 1200, 2, 3),
            ('2025-06-25', '21:00:00', 1200, 3, 1),
            ('2025-06-26', '19:00:00', 1200, 1, 1),
            ('2025-06-26', '21:30:00', 1200, 2, 1),
            ('2025-06-27', '18:30:00', 1200, 1, 3),
            ('2025-06-27', '20:30:00', 1200, 2, 2),
            ('2025-06-28', '17:00:00', 1000, 1, 2),
            ('2025-06-28', '19:30:00', 1200, 2, 1),
            ('2025-06-28', '22:00:00', 1500, 3, 3),
            ('2025-06-29', '16:00:00', 1000, 1, 1),
            ('2025-06-29', '18:30:00', 1200, 2, 2),
            ('2025-06-29', '21:00:00', 1200, 3, 3),
            ('2025-06-30', '19:00:00', 1200, 1, 2),
            ('2025-06-30', '21:30:00', 1200, 2, 3),
            ('2025-07-01', '20:00:00', 1200, 1, 1)
        """)
        
        # Insérer des tarifs par âge
        cursor.execute("""
            INSERT INTO ageprice (name, agemax, agemin, factor) VALUES 
            ('Enfant', 12, 0, 0.70),
            ('Adulte', 64, 13, 1.00),
            ('Senior', 120, 65, 0.80)
        """)
        
        connection.commit()
        print("Données de test insérées avec succès")
        
    except Error as e:
        print(f"Erreur lors de l'insertion des données de test: {e}")

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
    """Ajoute une nouvelle salle"""
    connection = get_db_connection()
    
    if connection is None:
        return False, "Erreur de connexion à la base de données"
        
    try:
        cursor = connection.cursor()
        
        cursor.execute("INSERT INTO room (name, nb_rows, nb_columns) VALUES (%s, %s, %s)", 
                      (name, nb_rows, nb_columns))
        room_id = cursor.lastrowid
        connection.commit()
        
        # Créer les sièges pour la nouvelle salle
        create_seats_for_room(cursor, connection, room_id, nb_rows, nb_columns)
        
        return True, f"Salle '{name}' ajoutée avec succès"
        
    except Error as e:
        return False, f"Erreur lors de l'ajout de la salle: {e}"
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def create_seats_for_room(cursor, connection, room_id, nb_rows, nb_columns):
    """Crée les sièges pour une salle donnée selon les dimensions spécifiées"""
    
    print(f"Création de {nb_rows * nb_columns} sièges ({nb_rows} rangées x {nb_columns} colonnes) pour la salle {room_id}")
    
    seats_created = 0
    
    for row_number in range(1, nb_rows + 1):
        # Convertir le numéro de rangée en lettre (1=A, 2=B, 3=C, etc.)
        row_letter = chr(64 + row_number)  # 65 = 'A', 66 = 'B', etc.
        
        print(f"  Rangée {row_letter}: {nb_columns} sièges")
        
        for seat_column in range(1, nb_columns + 1):
            # Tous les sièges sont normaux par défaut
            seat_type = 'normal'
            
            # Insérer le siège dans la base de données
            cursor.execute("""
                INSERT INTO seat (type, room_id, seat_row, seat_column) 
                VALUES (%s, %s, %s, %s)
            """, (seat_type, room_id, row_letter, seat_column))
            
            seats_created += 1
            
            # Debug : afficher chaque siège créé
            print(f"    Siège {row_letter}{seat_column} (NORMAL)")
    
    connection.commit()
    print(f"Total de {seats_created} sièges créés avec succès")
    
    return seats_created

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

# ===== FONCTIONS POUR LES SIÈGES ET RÉSERVATIONS =====

def get_seats_for_seance(seance_id):
    """Récupère tous les sièges d'une séance avec leur statut"""
    connection = get_db_connection()
    
    if connection is None:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.*, 
                   CASE WHEN sr.seat_id IS NOT NULL THEN 1 ELSE 0 END as occupied
            FROM seat s
            JOIN seance se ON s.room_id = se.room_id
            LEFT JOIN seatreservation sr ON s.id = sr.seat_id AND sr.seance_id = %s
            WHERE se.id = %s
            ORDER BY s.seat_row, s.seat_column
        """, (seance_id, seance_id))
        seats = cursor.fetchall()
        return seats
        
    except Error as e:
        print(f"Erreur lors de la récupération des sièges: {e}")
        return None
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def create_booking(account_id, seance_id, spectators_data):
    """Crée une réservation avec les spectateurs"""
    connection = get_db_connection()
    
    if connection is None:
        return False, "Erreur de connexion à la base de données"
        
    try:
        cursor = connection.cursor()
        
        # Calculer le prix total
        total_price = calculate_total_price(cursor, seance_id, spectators_data)
        
        # Créer la réservation
        cursor.execute("""
            INSERT INTO booking (price, account_id, seance_id) 
            VALUES (%s, %s, %s)
        """, (total_price, account_id, seance_id))
        booking_id = cursor.lastrowid
        
        # Ajouter chaque spectateur et sa réservation de siège
        for spectator in spectators_data:
            # Ajouter le spectateur
            cursor.execute("""
                INSERT INTO customer (firstname, lastname, age, pmr, booking_id) 
                VALUES (%s, %s, %s, %s, %s)
            """, (spectator['firstname'], spectator['lastname'], 
                 spectator['age'], spectator.get('pmr', 0), booking_id))
            customer_id = cursor.lastrowid
            
            # Réserver le siège
            cursor.execute("""
                INSERT INTO seatreservation (customer_id, seance_id, seat_id) 
                VALUES (%s, %s, %s)
            """, (customer_id, seance_id, spectator['seat_id']))
        
        connection.commit()
        return True, f"Réservation créée avec succès (Total: {total_price/100:.2f}€)"
        
    except Error as e:
        return False, f"Erreur lors de la création de la réservation: {e}"
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def calculate_total_price(cursor, seance_id, spectators_data):
    """Calcule le prix total d'une réservation"""
    # Récupérer le prix de base de la séance
    cursor.execute("SELECT baseprice FROM seance WHERE id = %s", (seance_id,))
    base_price = cursor.fetchone()[0]
    
    # Récupérer les tarifs par âge
    cursor.execute("SELECT * FROM ageprice ORDER BY agemin")
    age_prices = cursor.fetchall()
    
    total = 0
    for spectator in spectators_data:
        age = spectator['age']
        factor = 1.0  # Par défaut
        
        # Trouver le bon tarif selon l'âge
        for price_rule in age_prices:
            if price_rule[2] <= age <= price_rule[3]:  # agemin <= age <= agemax
                factor = float(price_rule[4])  # factor
                break
        
        total += base_price * factor
    
    return int(total)

def force_reset_database():
    """Force la réinitialisation complète de la base de données"""
    connection = get_db_connection()
    
    if connection:
        try:
            cursor = connection.cursor()
            
            # Créer la base de données si elle n'existe pas
            cursor.execute("CREATE DATABASE IF NOT EXISTS Cinemacousas")
            cursor.execute("USE Cinemacousas")
            
            print("Suppression de toutes les tables...")
            # Supprimer les tables dans le bon ordre (contraintes de clés étrangères)
            drop_tables = [
                "DROP TABLE IF EXISTS seatreservation",
                "DROP TABLE IF EXISTS customer", 
                "DROP TABLE IF EXISTS booking",
                "DROP TABLE IF EXISTS seat",
                "DROP TABLE IF EXISTS seance",
                "DROP TABLE IF EXISTS movie",
                "DROP TABLE IF EXISTS room",
                "DROP TABLE IF EXISTS account",
                "DROP TABLE IF EXISTS ageprice"
            ]
            
            for drop_cmd in drop_tables:
                cursor.execute(drop_cmd)
            
            print("Recréation des tables...")
            # Recréer les tables avec la nouvelle structure
            create_tables(cursor, connection)
            insert_test_data(cursor, connection)
            print("Base de données réinitialisée avec succès")
            
            return True
                
        except Error as e:
            print(f"Erreur lors de la réinitialisation de la base de données: {e}")
            return False
        
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    return False

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