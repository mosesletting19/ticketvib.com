from flask import Blueprint, request, jsonify, current_app
from models import db, Event
from werkzeug.utils import secure_filename
import os
from datetime import datetime, time

events_bp = Blueprint('events', __name__, url_prefix='/events')

# Create an event
@events_bp.route('/', methods=['POST'])
def add_event():
    data = request.form
    poster = request.files.get('poster')

    if 'title' not in data or 'date' not in data or 'venue' not in data or 'startTime' not in data or 'description' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    if poster:
        poster_filename = secure_filename(poster.filename)
        poster.save(os.path.join(current_app.config['UPLOAD_FOLDER'], poster_filename))
    else:
        poster_filename = None

    # Convert date string to date object
    event_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    # Convert time string to time object
    event_time = datetime.strptime(data['startTime'], '%H:%M').time()

    event = Event(
        title=data['title'],
        date=event_date,
        venue=data['venue'],
        start_time=event_time,
        description=data['description'],
        poster=poster_filename
    )
    db.session.add(event)
    db.session.commit()

    return jsonify({"message": "Event added successfully"}), 201

# Get all events
@events_bp.route('/', methods=['GET'])
def get_events():
    events = Event.query.all()
    events_list = [
        {
            "id": event.id,
            "title": event.title,
            "date": event.date.strftime('%Y-%m-%d'),
            "venue": event.venue,
            "start_time": event.start_time.strftime('%H:%M'),
            "description": event.description,
            "poster": event.poster
        }
        for event in events
    ]
    return jsonify(events_list)

# Get a specific event by ID
@events_bp.route('/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    event_data = {
        "id": event.id,
        "title": event.title,
        "date": event.date.strftime('%Y-%m-%d'),
        "venue": event.venue,
        "start_time": event.start_time.strftime('%H:%M'),
        "description": event.description,
        "poster": event.poster
    }
    return jsonify(event_data)

# Update an event by ID
@events_bp.route('/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    data = request.form
    poster = request.files.get('poster')

    if 'title' in data:
        event.title = data['title']
    if 'date' in data:
        event.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    if 'startTime' in data:
        event.start_time = datetime.strptime(data['startTime'], '%H:%M').time()
    if 'venue' in data:
        event.venue = data['venue']
    if 'description' in data:
        event.description = data['description']
    if poster:
        poster_filename = secure_filename(poster.filename)
        poster.save(os.path.join(current_app.config['UPLOAD_FOLDER'], poster_filename))
        event.poster = poster_filename

    db.session.commit()

    return jsonify({"message": "Event updated successfully"})

# Delete an event by ID
@events_bp.route('/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    db.session.delete(event)
    db.session.commit()

    return jsonify({"message": "Event deleted successfully"})
