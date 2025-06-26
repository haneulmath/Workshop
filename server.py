#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash, Response
from flask_cors import CORS
import modele  # Import du module pour la gestion de la base de données
import importlib
from datetime import datetime
import json
import time

# Forcer le rechargement du module modele
importlib.reload(modele)

app = Flask(__name__)
CORS(app)
app.secret_key = 'your-secret-key-here'  # Changez cette clé en production

# Cache timestamp pour le cache-busting des affiches
POSTER_CACHE_TIMESTAMP = str(int(time.time()))

def get_poster_url_with_cache_busting(movie_id):
    """Génère une URL d'affiche avec paramètre de cache-busting"""
    return url_for('movie_poster', movie_id=movie_id, v=POSTER_CACHE_TIMESTAMP)

# Rendre la fonction disponible dans les templates
@app.context_processor
def utility_processor():
    return dict(get_poster_url_with_cache_busting=get_poster_url_with_cache_busting)

# Ajouter des fonctions helper pour les templates
@app.template_global()
def chr_function(num):
    return chr(num)

@app.route('/')
def index():
    """Page d'accueil - Redirection vers home"""
    return redirect(url_for('home'))

@app.route('/home')
def home():
    """Page d'accueil principale"""
    # Récupérer les séances d'aujourd'hui pour l'aperçu
    showings_today = modele.get_showings_today()
    
    # Récupérer tous les films à l'affiche
    movies = modele.get_all_movies()
    
    return render_template('home.html', showings_today=showings_today, movies=movies)

@app.route('/movies')
def movies():
    """Page des films"""
    movies = modele.get_all_movies()
    if movies is None:
        flash('Erreur lors de la récupération des films', 'error')
        return redirect(url_for('home'))
    return render_template('movies.html', movies=movies)

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    """Page de détail d'un film avec ses séances"""
    movie = modele.get_movie_by_id(movie_id)
    if not movie:
        flash('Film non trouvé', 'error')
        return redirect(url_for('movies'))
    
    showings = modele.get_showings_by_movie(movie_id)
    if showings is None:
        flash('Erreur lors de la récupération des séances', 'error')
        return redirect(url_for('movies'))
    
    return render_template('movie_detail.html', movie=movie, showings=showings)

@app.route('/movie/<int:movie_id>/poster')
def movie_poster(movie_id):
    """Servir l'affiche d'un film en tant qu'image"""
    poster = modele.get_movie_poster(movie_id)
    
    if not poster:
        # Retourner une image par défaut ou une erreur 404
        return Response("Affiche non trouvée", status=404)
    
    # Vérifier si c'est une requête avec cache-busting
    version = request.args.get('v', '')
    
    # Cache plus court pour permettre les mises à jour
    cache_control = 'public, max-age=300'  # Cache 5 minutes
    if version:
        # Si version spécifiée, cache plus long mais avec ETag
        cache_control = 'public, max-age=3600'  # Cache 1 heure avec version
    
    return Response(
        poster['image'],
        mimetype=poster['mime_type'],
        headers={
            'Content-Disposition': f'inline; filename="{poster["name"]}"',
            'Cache-Control': cache_control,
            'ETag': f'"{movie_id}-{len(poster["image"])}"'  # ETag basé sur l'ID et la taille
        }
    )

@app.route('/showings/today')
def showings_today():
    """Page des séances d'aujourd'hui"""
    showings = modele.get_showings_today()
    if showings is None:
        flash('Erreur lors de la récupération des séances', 'error')
        return redirect(url_for('home'))
    return render_template('showings_today.html', showings=showings)

@app.route('/showing/<int:showing_id>/seats')
def showing_seats(showing_id):
    """Page de sélection des sièges pour une séance"""
    # Récupérer les informations de la séance
    showing = modele.get_showing_by_id(showing_id)
    if not showing:
        flash('Séance non trouvée', 'error')
        return redirect(url_for('showings_today'))
    
    # Récupérer les informations de la salle et la grille de sièges
    seats_data = modele.get_showing_seats_grid(showing_id)
    if not seats_data:
        flash('Erreur lors de la récupération des sièges', 'error')
        return redirect(url_for('showings_today'))
    
    room = seats_data['room']
    grid = seats_data['grid']
    
    return render_template('showing_seats.html', 
                         showing=showing, 
                         room=room, 
                         grid=grid)

@app.route('/booking', methods=['POST'])
def book_seats():
    """Rediriger vers le formulaire d'informations des spectateurs"""
    showing_id = request.form.get('showing_id')
    selected_seats = request.form.get('selected_seats')
    
    if not showing_id or not selected_seats:
        flash('Données de réservation manquantes', 'error')
        return redirect(url_for('showings_today'))
    
    try:
        showing_id = int(showing_id)
        seat_ids = json.loads(selected_seats)
        
        if not seat_ids:
            flash('Aucune place sélectionnée', 'error')
            return redirect(url_for('showing_seats', showing_id=showing_id))
        
        # Récupérer les informations de la séance et des places
        showing = modele.get_showing_by_id(showing_id)
        if not showing:
            flash('Séance non trouvée', 'error')
            return redirect(url_for('showings_today'))
        
        selected_seats_details = []
        for seat_id in seat_ids:
            seat = modele.get_seat_by_id(seat_id)
            if seat:
                selected_seats_details.append(seat)
        
        if not selected_seats_details:
            flash('Places non trouvées', 'error')
            return redirect(url_for('showing_seats', showing_id=showing_id))
        
        # Rediriger vers le formulaire d'informations des spectateurs
        return render_template('booking_spectators.html',
                             showing=showing,
                             selected_seats=selected_seats_details,
                             selected_seats_json=selected_seats)
        
    except (ValueError, json.JSONDecodeError) as e:
        flash('Données de réservation invalides', 'error')
        return redirect(url_for('showing_seats', showing_id=showing_id))

@app.route('/booking/spectators', methods=['POST'])
def process_spectators_info():
    """Traiter les informations des spectateurs et finaliser la réservation"""
    showing_id = request.form.get('showing_id')
    selected_seats = request.form.get('selected_seats')
    spectators_data = {}
    
    # Récupérer les données des spectateurs du formulaire
    for key, value in request.form.items():
        if key.startswith('spectators['):
            # Parse spectators[0][first_name] => index 0, field first_name
            import re
            match = re.match(r'spectators\[(\d+)\]\[(\w+)\]', key)
            if match:
                index = int(match.group(1))
                field = match.group(2)
                if index not in spectators_data:
                    spectators_data[index] = {}
                spectators_data[index][field] = value
    
    if not showing_id or not selected_seats:
        flash('Données de réservation manquantes', 'error')
        return redirect(url_for('showings_today'))
    
    try:
        showing_id = int(showing_id)
        seat_ids = json.loads(selected_seats)
        
        # Valider que nous avons des informations pour chaque spectateur
        if len(spectators_data) != len(seat_ids):
            flash('Informations des spectateurs incomplètes', 'error')
            return redirect(url_for('showing_seats', showing_id=showing_id))
        
        # Calculer le prix total
        showing = modele.get_showing_by_id(showing_id)
        total_price = 0
        booking_details = []
        
        for i, seat_id in enumerate(seat_ids):
            if i not in spectators_data:
                flash('Informations manquantes pour certains spectateurs', 'error')
                return redirect(url_for('showing_seats', showing_id=showing_id))
            
            spectator = spectators_data[i]
            age = int(spectator.get('age', 0))
            
            # Calculer le prix selon l'âge
            price_discount = 1.0
            if age <= 12:
                price_discount = 0.5  # Enfant
            elif age <= 17:
                price_discount = 0.7  # Jeune
            elif age <= 25:
                price_discount = 0.8  # Étudiant
            elif age >= 65:
                price_discount = 0.6  # Senior
            
            seat_price = showing['price'] * price_discount
            total_price += seat_price
            
            seat = modele.get_seat_by_id(seat_id)
            booking_details.append({
                'seat': seat,
                'spectator': spectator,
                'price': seat_price
            })
        
        # Effectuer la réservation avec les informations des spectateurs
        success, result = modele.book_seats_with_spectators(
            showing_id, 
            seat_ids, 
            spectators_data,
            session.get('user_id', 1),
            total_price
        )
        
        if success:
            return render_template('booking_tickets.html',
                                 success=True,
                                 booking_id=result['booking_id'],
                                 booking=result['booking'],
                                 showing=showing,
                                 booking_details=booking_details,
                                 total_price=total_price)
        else:
            flash(f'Erreur lors de la réservation: {result}', 'error')
            return redirect(url_for('showing_seats', showing_id=showing_id))
        
    except (ValueError, json.JSONDecodeError) as e:
        flash('Données de réservation invalides', 'error')
        return redirect(url_for('showing_seats', showing_id=showing_id))

# ===== ROUTES D'AUTHENTIFICATION =====

@app.route('/login', methods=['GET', 'POST'])
def login_form():
    """Formulaire de connexion et traitement"""
    if request.method == 'GET':
        return render_template('login.html')
    
    # POST - traitement de la connexion
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
    
    if not username or not password:
        if request.is_json:
            return jsonify({'success': False, 'message': 'Nom d\'utilisateur et mot de passe requis'}), 400
        else:
            flash('Nom d\'utilisateur et mot de passe requis', 'error')
            return redirect(url_for('login_form'))
    
    # Pour simplifier, on accepte n'importe quel nom d'utilisateur avec un mot de passe
    # En production, utilisez une vraie authentification
    if password:  # Simple vérification non-vide
        session['user_id'] = 1  # ID utilisateur fictif
        session['username'] = username
        if request.is_json:
            return jsonify({'success': True, 'message': 'Connexion réussie'})
        else:
            flash('Connexion réussie', 'success')
            return redirect(url_for('home'))
    else:
        if request.is_json:
            return jsonify({'success': False, 'message': 'Mot de passe incorrect'}), 401
        else:
            flash('Mot de passe incorrect', 'error')
            return redirect(url_for('login_form'))

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

@app.route('/api/movie/<int:movie_id>/showings')
def get_movie_showings(movie_id):
    """API pour récupérer toutes les séances d'un film spécifique"""
    showings = modele.get_showings_by_movie(movie_id)
    if showings is None:
        return jsonify({'error': 'Erreur lors de la récupération des séances'}), 500
    
    # Formater les données pour le frontend
    formatted_showings = []
    for showing in showings:
        formatted_showings.append({
            'id': showing['id'],
            'date': showing['date'].strftime('%Y-%m-%d'),
            'time': str(showing['starttime']),
            'room': showing['room_name'],
            'price': showing['baseprice'] / 100,  # Convertir centimes en euros
            'movie_name': showing['movie_name']
        })
    
    return jsonify(formatted_showings)

@app.route('/api/showings/today')
def get_showings_today():
    """API pour récupérer les séances d'aujourd'hui"""
    showings = modele.get_showings_today()
    if showings is None:
        return jsonify({'error': 'Erreur lors de la récupération des séances'}), 500
    
    # Formater les données pour le frontend
    formatted_showings = []
    for showing in showings:
        formatted_showings.append({
            'id': showing['id'],
            'movie': showing['movie_name'],
            'time': str(showing['starttime']),
            'room': showing['room_name'],
            'price': showing['baseprice'] / 100  # Convertir centimes en euros
        })
    
    return jsonify(formatted_showings)

@app.route('/api/showing/<int:showing_id>/seats')
def get_showing_seats(showing_id):
    """API pour récupérer les sièges d'une séance avec la même structure que l'admin"""
    seats = modele.get_seats_for_showing(showing_id)
    if seats is None:
        return jsonify({'error': 'Erreur lors de la récupération des sièges'}), 500
    
    # Récupérer les informations de la salle pour cette séance
    showing_info = modele.get_showing_info(showing_id)
    if showing_info is None:
        return jsonify({'error': 'Séance non trouvée'}), 404
    
    # Organiser les sièges en grille comme l'interface d'administration
    grid = {}
    for seat in seats:
        row = seat['seat_row']
        if row not in grid:
            grid[row] = {}
        grid[row][seat['seat_column']] = {
            'id': seat['id'],
            'type': seat['type'],
            'occupied': bool(seat['occupied'])
        }
    
    return jsonify({
        'room': {
            'id': showing_info['room_id'],
            'name': showing_info['room_name'],
            'nb_rows': showing_info['nb_rows'],
            'nb_columns': showing_info['nb_columns']
        },
        'grid': grid
    })

@app.route('/api/booking', methods=['POST'])
def create_booking():
    """API pour créer une réservation"""
    data = request.get_json()
    
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Vous devez être connecté'}), 401
    
    showing_id = data.get('showing_id')
    spectators = data.get('spectators')
    
    if not showing_id or not spectators:
        return jsonify({'success': False, 'message': 'Données manquantes'}), 400
    
    # Créer la réservation
    success, message = modele.create_booking(session['user_id'], showing_id, spectators)
    
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
    showings = modele.get_all_showings()
    bookings = modele.get_all_bookings()
    
    # Ajouter la date actuelle pour les statistiques
    from datetime import date
    today = date.today()
    
    return render_template('admin.html', movies=movies, rooms=rooms, showings=showings, bookings=bookings, today=today)

@app.route('/admin/movie', methods=['POST'])
def add_movie():
    """Ajouter un film"""
    name = request.form.get('name')
    duration = request.form.get('duration')
    director = request.form.get('director')
    cast = request.form.get('cast')
    synopsis = request.form.get('synopsis')
    
    if not name or not duration:
        flash('Nom et durée du film requis', 'error')
        return redirect(url_for('admin_dashboard'))
    
    try:
        duration = int(duration)
        success, message = modele.add_movie(name, duration, director, cast, synopsis)
        flash(message, 'success' if success else 'error')
    except ValueError:
        flash('La durée doit être un nombre', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/movie/<int:movie_id>/update', methods=['POST'])
def update_movie(movie_id):
    """Mettre à jour un film"""
    name = request.form.get('name')
    duration = request.form.get('duration')
    director = request.form.get('director')
    cast = request.form.get('cast')
    synopsis = request.form.get('synopsis')
    
    if not name or not duration:
        flash('Nom et durée du film requis', 'error')
        return redirect(url_for('admin_dashboard'))
    
    try:
        duration = int(duration)
        success, message = modele.update_movie(movie_id, name, duration, director, cast, synopsis)
        flash(message, 'success' if success else 'error')
    except ValueError:
        flash('La durée doit être un nombre', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/movie/<int:movie_id>/delete', methods=['POST'])
def delete_movie(movie_id):
    """Supprimer un film"""
    success, message = modele.delete_movie(movie_id)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/movie/<int:movie_id>/poster/upload', methods=['POST'])
def upload_movie_poster(movie_id):
    """Télécharger une affiche pour un film"""
    try:
        if 'poster' not in request.files:
            flash('Aucun fichier sélectionné', 'error')
            return redirect(url_for('admin_dashboard'))
        
        file = request.files['poster']
        if file.filename == '':
            flash('Aucun fichier sélectionné', 'error')
            return redirect(url_for('admin_dashboard'))
        
        # Vérifier le type de fichier
        allowed_types = {'image/jpeg', 'image/png', 'image/svg+xml'}
        if file.content_type not in allowed_types:
            flash('Type de fichier non supporté. Utilisez JPG, PNG ou SVG.', 'error')
            return redirect(url_for('admin_dashboard'))
        
        # Vérifier la taille (5MB max)
        file.seek(0, 2)  # Se déplacer à la fin du fichier
        file_size = file.tell()
        file.seek(0)  # Revenir au début
        
        if file_size > 5 * 1024 * 1024:  # 5MB
            flash('Le fichier est trop volumineux (max 5MB)', 'error')
            return redirect(url_for('admin_dashboard'))
        
        # Lire le contenu du fichier
        file_content = file.read()
        
        # Sauvegarder l'affiche
        success, message = modele.save_movie_poster(movie_id, file.filename, file.content_type, file_content)
        
        # Mettre à jour le timestamp du cache pour forcer le rafraîchissement
        if success:
            global POSTER_CACHE_TIMESTAMP
            POSTER_CACHE_TIMESTAMP = str(int(time.time()))
        
        flash(message, 'success' if success else 'error')
        
    except Exception as e:
        flash(f'Erreur lors du téléchargement: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/movie/<int:movie_id>/poster/delete', methods=['POST'])
def delete_movie_poster_route(movie_id):
    """Supprimer l'affiche d'un film"""
    success, message = modele.delete_movie_poster(movie_id)
    
    # Mettre à jour le timestamp du cache pour forcer le rafraîchissement
    if success:
        global POSTER_CACHE_TIMESTAMP
        POSTER_CACHE_TIMESTAMP = str(int(time.time()))
    
    flash(message, 'success' if success else 'error')
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

@app.route('/admin/room/<int:room_id>/update', methods=['POST'])
def update_room(room_id):
    """Mettre à jour une salle"""
    name = request.form.get('name')
    nb_rows = request.form.get('rows')
    nb_columns = request.form.get('columns')
    
    if not name:
        flash('Nom de la salle requis', 'error')
        return redirect(url_for('admin_dashboard'))
    
    # Si les dimensions ne sont pas fournies, utiliser les valeurs actuelles
    if not nb_rows or not nb_columns:
        # Récupérer les dimensions actuelles
        rooms = modele.get_all_rooms()
        current_room = next((room for room in rooms if room['id'] == room_id), None)
        if current_room:
            nb_rows = current_room['nb_rows']
            nb_columns = current_room['nb_columns']
        else:
            flash('Salle non trouvée', 'error')
            return redirect(url_for('admin_dashboard'))
    
    try:
        nb_rows = int(nb_rows)
        nb_columns = int(nb_columns)
        success, message = modele.update_room(room_id, name, nb_rows, nb_columns)
        flash(message, 'success' if success else 'error')
    except ValueError:
        flash('Le nombre de rangées et colonnes doit être un nombre', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/room/<int:room_id>/delete', methods=['POST'])
def delete_room(room_id):
    """Supprimer une salle"""
    success, message = modele.delete_room(room_id)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/showing', methods=['POST'])
def add_showing():
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
        
        success, message = modele.add_showing(date, starttime, baseprice, room_id, movie_id)
        flash(message, 'success' if success else 'error')
    except ValueError:
        flash('Données invalides', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/showing/<int:showing_id>/update', methods=['POST'])
def update_showing(showing_id):
    """Mettre à jour une séance"""
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
        
        success, message = modele.update_showing(showing_id, date, starttime, baseprice, room_id, movie_id)
        flash(message, 'success' if success else 'error')
    except ValueError:
        flash('Données invalides', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/showing/<int:showing_id>/delete', methods=['POST'])
def delete_showing(showing_id):
    """Supprimer une séance"""
    success, message = modele.delete_showing(showing_id)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/booking/<int:booking_id>/cancel', methods=['POST'])
def cancel_booking(booking_id):
    """Annuler une réservation"""
    success, message = modele.cancel_booking(booking_id)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/my-bookings')
def my_bookings():
    """Afficher les réservations de l'utilisateur connecté"""
    if 'user_id' not in session:
        flash('Vous devez être connecté pour voir vos réservations', 'error')
        return redirect(url_for('login_form'))
    
    user_id = session['user_id']
    bookings = modele.get_user_bookings(user_id)
    
    # Ajouter la date actuelle pour les comparaisons dans le template
    from datetime import date
    today = date.today()
    
    # Convertir les dates datetime en date pour la comparaison
    for booking in bookings:
        if hasattr(booking['date'], 'date'):
            booking['date_only'] = booking['date'].date()
        else:
            booking['date_only'] = booking['date']
    
    return render_template('my_bookings.html', bookings=bookings, today=today)

@app.route('/booking/<int:booking_id>/details')
def booking_details(booking_id):
    """Afficher les détails d'une réservation spécifique avec réimpression des billets"""
    if 'user_id' not in session:
        flash('Vous devez être connecté pour voir cette réservation', 'error')
        return redirect(url_for('login_form'))
    
    user_id = session['user_id']
    booking = modele.get_booking_details(booking_id, user_id)
    
    if not booking:
        flash('Réservation non trouvée', 'error')
        return redirect(url_for('my_bookings'))
    
    # Calculer les prix individuels selon l'âge (comme dans la réservation originale)
    booking_details = []
    for seat_detail in booking['seats_details']:
        age = seat_detail['age']
        
        # Calculer le prix selon l'âge (en utilisant le prix de base de la séance)
        # On utilise une estimation du prix de base à partir du prix total
        base_price = booking['price_euros'] / len(booking['seats_details'])
        
        price_discount = 1.0
        if age <= 12:
            price_discount = 0.5  # Enfant
        elif age <= 17:
            price_discount = 0.7  # Jeune
        elif age <= 25:
            price_discount = 0.8  # Étudiant
        elif age >= 65:
            price_discount = 0.6  # Senior
        
        seat_price = base_price * price_discount
        
        booking_details.append({
            'seat': seat_detail,
            'spectator': {
                'first_name': seat_detail['firstname'],
                'last_name': seat_detail['lastname'],
                'age': seat_detail['age']
            },
            'price': seat_price
        })
    
    # Préparer l'objet showing pour compatibilité avec le template booking_tickets
    showing = {
        'id': booking['showing_id'],
        'movie': booking['movie_name'],
        'date': booking['date'],
        'time': booking['time'],
        'room': booking['room_name']
    }
    
    return render_template('booking_tickets.html',
                         success=True,
                         booking_id=booking['booking_id'],
                         booking=booking,
                         showing=showing,
                         booking_details=booking_details,
                         total_price=booking['price_euros'],
                         is_reprint=True)

# Point d'entrée du programme
if __name__ == "__main__":
    print("Démarrage du serveur Flask sur le port 5002...")
    app.run(debug=True, port=5002)