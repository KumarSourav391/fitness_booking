from app import create_app, db
from app.models import FitnessClass
from datetime import datetime, timedelta
from pytz import timezone

app = create_app("local")

with app.app_context():
    db.drop_all()
    db.create_all()

    ist = timezone("Asia/Kolkata")
    now = datetime.now(ist)

    classes = [
        FitnessClass(name="Yoga", datetime_ist=now + timedelta(days=1), instructor="Aniya Shetty", available_slots=7),
        FitnessClass(name="Zumba", datetime_ist=now + timedelta(days=2), instructor="Rahul Vaidya", available_slots=10),
        FitnessClass(name="HIIT", datetime_ist=now + timedelta(days=3), instructor="Sneha Tiwari", available_slots=12),
    ]

    db.session.bulk_save_objects(classes)
    db.session.commit()
    print("Seeded sample fitness classes.")