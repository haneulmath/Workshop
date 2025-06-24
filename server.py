#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from flask_cors import CORS
import old.modele as modele  # Import du module pour la gestion de la base de données
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'votre_clef_secrete_cinema'  # Changez ceci en production
CORS(app)

@app.route('/')
def index():
    """Page d'accueil - Interface de réservation"""
    return render_template('index.html')

# ===== ROUTES D'AUTHENTIFICATION =====

@app.route('/login', methods=['POST'])
def login():
    """Connexion utilisateur"""
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
    
    if not username or not password:
        return jsonify({'success': False, 'message': 'Nom d\'utilisateur et mot de passe requis'}), 400
    
    # Pour simplifier, on accepte n'importe quel nom d'utilisateur avec un mot de passe
    # En production, utilisez une vraie authentification
    if password:  # Simple vérification non-vide
        session['user_id'] = 1  # ID utilisateur fictif
        session['username'] = username
        return jsonify({'success': True, 'message': 'Connexion réussie'})
    else:
        return jsonify({'success': False, 'message': 'Mot de passe incorrect'}), 401

@app.route('/logout')
def logout():
    """Déconnexion utilisateur"""
    session.clear()
    return redirect(url_for('index'))

# ===== ROUTES API POUR LES DONNÉES =====

@app.route('/api/movies')
def get_movies():
    """API pour récupérer tous les films"""
    movies = modele.get_all_movies()
    if movies is None:
        return jsonify({'error': 'Erreur lors de la récupération des films'}), 500
    return jsonify(movies)

@app.route('/api/movie/<int:movie_id>/seances')
def get_movie_seances(movie_id):
    """API pour récupérer toutes les séances d'un film spécifique"""
    seances = modele.get_seances_by_movie(movie_id)
    if seances is None:
        return jsonify({'error': 'Erreur lors de la récupération des séances'}), 500
    
    # Formater les données pour le frontend
    formatted_seances = []
    for seance in seances:
        formatted_seances.append({
            'id': seance['id'],
            'date': seance['date'].strftime('%Y-%m-%d'),
            'time': str(seance['starttime']),
            'room': seance['room_name'],
            'price': seance['baseprice'] / 100,  # Convertir centimes en euros
            'movie_name': seance['movie_name']
        })
    
    return jsonify(formatted_seances)

@app.route('/api/seances/today')
def get_seances_today():
    """API pour récupérer les séances d'aujourd'hui"""
    seances = modele.get_seances_today()
    if seances is None:
        return jsonify({'error': 'Erreur lors de la récupération des séances'}), 500
    
    # Formater les données pour le frontend
    formatted_seances = []
    for seance in seances:
        formatted_seances.append({
            'id': seance['id'],
            'movie': seance['movie_name'],
            'time': str(seance['starttime']),
            'room': seance['room_name'],
            'price': seance['baseprice'] / 100  # Convertir centimes en euros
        })
    
    return jsonify(formatted_seances)

@app.route('/api/seance/<int:seance_id>/seats')
def get_seance_seats(seance_id):
    """API pour récupérer les sièges d'une séance"""
    seats = modele.get_seats_for_seance(seance_id)
    if seats is None:
        return jsonify({'error': 'Erreur lors de la récupération des sièges'}), 500
    
    # Formater les sièges pour le frontend
    formatted_seats = []
    for seat in seats:
        formatted_seats.append({
            'id': seat['id'],
            'row': seat['seat_row'],
            'column': seat['seat_column'],
            'type': seat['type'],  # nouveau champ: normal, pmr, stair, empty
            'occupied': bool(seat['occupied']),
            'label': f"{seat['seat_column']}{seat['seat_column']}"  # A1, A2, etc.
        })
    
    return jsonify(formatted_seats)

@app.route('/api/booking', methods=['POST'])
def create_booking():
    """API pour créer une réservation"""
    data = request.get_json()
    
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Vous devez être connecté'}), 401
    
    seance_id = data.get('seance_id')
    spectators = data.get('spectators')
    
    if not seance_id or not spectators:
        return jsonify({'success': False, 'message': 'Données manquantes'}), 400
    
    # Créer la réservation
    success, message = modele.create_booking(session['user_id'], seance_id, spectators)
    
    return jsonify({'success': success, 'message': message})

# ===== ROUTES POUR LA GESTION DES SIÈGES =====

@app.route('/api/room/<int:room_id>/seats')
def get_room_seats_grid(room_id):
    """API pour récupérer la grille des sièges d'une salle"""
    grid_data = modele.get_room_seats_grid(room_id)
    if grid_data is None:
        return jsonify({'error': 'Salle non trouvée'}), 404
    
    return jsonify(grid_data)

@app.route('/api/seat/<int:seat_id>/type', methods=['PUT'])
def update_seat_type(seat_id):
    """API pour mettre à jour le type d'un siège"""
    data = request.get_json()
    new_type = data.get('type')
    
    if new_type not in ['normal', 'pmr', 'stair', 'empty']:
        return jsonify({'success': False, 'message': 'Type de siège invalide'}), 400
    
    success, message = modele.update_seat_type(seat_id, new_type)
    return jsonify({'success': success, 'message': message})

# ===== ROUTES D'ADMINISTRATION =====

@app.route('/admin')
def admin_dashboard():
    """Tableau de bord administrateur"""
    movies = modele.get_all_movies()
    rooms = modele.get_all_rooms()
    seances = modele.get_all_seances()
    
    return render_template('admin.html', movies=movies, rooms=rooms, seances=seances)

@app.route('/admin/movie', methods=['POST'])
def add_movie():
    """Ajouter un film"""
    name = request.form.get('name')
    duration = request.form.get('duration')
    
    if not name or not duration:
        flash('Nom et durée du film requis', 'error')
        return redirect(url_for('admin_dashboard'))
    
    try:
        duration = int(duration)
        success, message = modele.add_movie(name, duration)
        flash(message, 'success' if success else 'error')
    except ValueError:
        flash('La durée doit être un nombre', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/room', methods=['POST'])
def add_room():
    """Ajouter une salle"""
    name = request.form.get('name')
    nb_rows = request.form.get('rows')
    nb_columns = request.form.get('columns')
    
    if not name or not nb_rows or not nb_columns:
        flash('Nom, nombre de rangées et colonnes requis', 'error')
        return redirect(url_for('admin_dashboard'))
    
    try:
        nb_rows = int(nb_rows)
        nb_columns = int(nb_columns)
        success, message = modele.add_room(name, nb_rows, nb_columns)
        flash(message, 'success' if success else 'error')
    except ValueError:
        flash('Le nombre de rangées et colonnes doit être un nombre', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/seance', methods=['POST'])
def add_seance():
    """Ajouter une séance"""
    date = request.form.get('date')
    starttime = request.form.get('starttime')
    baseprice = request.form.get('baseprice')
    room_id = request.form.get('room_id')
    movie_id = request.form.get('movie_id')
    
    if not all([date, starttime, baseprice, room_id, movie_id]):
        flash('Tous les champs sont requis', 'error')
        return redirect(url_for('admin_dashboard'))
    
    try:
        baseprice = int(float(baseprice) * 100)  # Convertir euros en centimes
        room_id = int(room_id)
        movie_id = int(movie_id)
        
        success, message = modele.add_seance(date, starttime, baseprice, room_id, movie_id)
        flash(message, 'success' if success else 'error')
    except ValueError:
        flash('Données invalides', 'error')
    
    return redirect(url_for('admin_dashboard'))

# Point d'entrée du programme
if __name__ == "__main__":
    # Initialisation de la base de données au démarrage
    print("Initialisation de la base de données cinema...")
    modele.initialize_database()
    
    print("Démarrage du serveur Flask sur le port 5001...")
    app.run(debug=True, port=5002)