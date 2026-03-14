# seed_incidents.py
# Run this file with: python seed_incidents.py

import random
from datetime import datetime, timedelta
from app import app, db, User, IncidentReport

NUM_RECORDS = 500
DAYS_RANGE = 365

LOCATIONS = [
    (40.7589, -73.9851),  # Times Square
    (40.7614, -73.9776),  # Central Park
    (40.7128, -74.0060),  # Downtown Manhattan
    (40.7484, -73.9857),  # Empire State Building
    (40.7580, -73.9855),  # Broadway
    (40.7489, -73.9680),  # Queens Plaza
    (40.6782, -73.9442),  # Brooklyn
    (40.7306, -73.9352)   # Williamsburg
]

INCIDENT_TYPES = ["harassment", "theft", "stalking", "assault", "verbal_abuse", "other"]
INCIDENT_WEIGHTS = [30, 20, 15, 10, 15, 10]

SEVERITY_LEVELS = [1, 2, 3, 4, 5]
SEVERITY_WEIGHTS = [5, 15, 40, 30, 10]

def random_time_within(days=DAYS_RANGE):
    now = datetime.utcnow()
    delta_days = random.randint(0, days)
    delta_seconds = random.randint(0, 86400)
    return now - timedelta(days=delta_days, seconds=delta_seconds)

def jitter(coord, max_jitter=0.0015):
    lat, lon = coord
    return lat + random.uniform(-max_jitter, max_jitter), lon + random.uniform(-max_jitter, max_jitter)

def main():
    with app.app_context():

        # Ensure one user exists
        user = User.query.first()
        if not user:
            user = User(
                username="demo_user",
                email="demo@example.com",
                phone="+10000000000"
            )
            db.session.add(user)
            db.session.commit()
            print(f"[OK] Created demo user (id={user.id})")

        existing = db.session.query(IncidentReport).count()
        print(f"[INFO] Existing incidents: {existing}")

        if existing >= NUM_RECORDS:
            print("[OK] Dataset already seeded.")
            return

        records_left = NUM_RECORDS - existing
        created = 0

        while created < records_left:
            batch = []
            for _ in range(100):
                base_lat, base_lon = random.choice(LOCATIONS)
                lat, lon = jitter((base_lat, base_lon))

                incident_type = random.choices(INCIDENT_TYPES, weights=INCIDENT_WEIGHTS, k=1)[0]
                severity = random.choices(SEVERITY_LEVELS, weights=SEVERITY_WEIGHTS, k=1)[0]

                time_of_incident = random_time_within()
                reported_at = time_of_incident + timedelta(minutes=random.randint(5, 1440))

                ir = IncidentReport(
                    user_id=user.id,
                    latitude=lat,
                    longitude=lon,
                    incident_type=incident_type,
                    severity=int(severity),
                    description=f"Simulated {incident_type} incident.",
                    time_of_incident=time_of_incident,
                    reported_at=reported_at
                )
                batch.append(ir)

            db.session.bulk_save_objects(batch)
            db.session.commit()
            created += len(batch)
            print(f"[SEED] Created {created}/{records_left} incident records...")

        print("[DONE] Seeding complete!")

if __name__ == "__main__":
    main()
