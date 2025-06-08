from flask import Blueprint, request, jsonify
from ..models import FitnessClass, Booking
from ..utils import convert_ist_to_timezone
classes_bp = Blueprint('classes_bp', __name__)


@classes_bp.route('/classes', methods=['GET'])
def get_classes():
    timezone = request.args.get('timezone', 'Asia/Kolkata')
    classes = FitnessClass.query.all()
    result = [{
        'id': c.id,
        'name': c.name,
        'datetime': convert_ist_to_timezone(c.datetime_ist, timezone).isoformat(),
        'instructor': c.instructor,
        'available_slots': c.available_slots
    } for c in classes]
    return jsonify(result), 200