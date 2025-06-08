from flask import Blueprint, request, jsonify
from ..models import FitnessClass, Booking
from .. import db
from ..utils import convert_ist_to_timezone
from datetime import datetime

booking_bp = Blueprint('booking_bp', __name__)

@booking_bp.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Fitness Studio Booking API!"})


@booking_bp.route('/book', methods=['POST'])
def book():
    data = request.get_json()
    if not data or not all(k in data for k in ('class_id', 'client_name', 'client_email')):
        return jsonify({'error': 'Missing required fields'}), 400

    fitness_class = FitnessClass.query.get(data['class_id'])
    if not fitness_class:
        return jsonify({'error': 'Class not found'}), 404
    if fitness_class.available_slots <= 0:
        return jsonify({'error': 'Class is fully booked'}), 400

    booking = Booking(
        class_id=data['class_id'],
        client_name=data['client_name'],
        client_email=data['client_email']
    )
    fitness_class.available_slots -= 1
    db.session.add(booking)
    db.session.commit()

    return jsonify({'message': 'Booking successful'}), 201

@booking_bp.route('/bookings', methods=['GET'])
def get_bookings():
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'Email parameter required'}), 400
    bookings = Booking.query.filter_by(client_email=email).all()
    result = [{
        'class_name': b.fitness_class.name,
        'datetime': b.fitness_class.datetime_ist.isoformat(),
        'instructor': b.fitness_class.instructor,
        "class_id": b.class_id,
        "client_name": b.client_name,
        "client_email": b.client_email
    } for b in bookings]
    return jsonify(result), 200