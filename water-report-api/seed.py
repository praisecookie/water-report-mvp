# seed.py
import random
from datetime import timedelta, date
from faker import Faker
from database import SessionLocal
import models

fake = Faker()
db = SessionLocal()

# Water Industry Roles & Certifications
ROLES = ["Water Treatment Operator", "Field Technician",
         "Maintenance Engineer", "Pump Station Inspector", "Compliance Officer"]
CERTIFICATIONS = ["OSHA 30", "Grade II Water Treatment",
                  "Confined Space Entry", "Hazardous Waste Operations", "CPR/First Aid"]
REGIONS = ["North District", "South District", "East Plant", "West Plant"]


def seed_database():
    print("Clearing old data...")
    db.query(models.WorkOrder).delete()
    db.query(models.Certification).delete()
    db.query(models.Technician).delete()
    db.commit()

    print("Generating Technicians...")
    technicians = []
    for _ in range(100):
        tech = models.Technician(
            name=fake.name(),
            role=random.choice(ROLES),
            region=random.choice(REGIONS)
        )
        db.add(tech)
        technicians.append(tech)
    db.commit()

    print("Generating Certifications & Work Orders...")
    for tech in technicians:
        # Give each tech 1-3 certifications
        for _ in range(random.randint(1, 3)):
            # 20% chance the cert is expired (to make our dashboard interesting)
            days_offset = random.randint(-60, 365)
            expiry = date.today() + timedelta(days=days_offset)

            cert = models.Certification(
                name=random.choice(CERTIFICATIONS),
                expiry_date=expiry,
                is_active=days_offset > 0,
                technician_id=tech.id
            )
            db.add(cert)

        # Give each tech 2-5 work orders over the next 52 weeks
        for _ in range(random.randint(2, 5)):
            scheduled = date.today() + timedelta(days=random.randint(1, 365))
            order = models.WorkOrder(
                task_description=f"{fake.bs().title()} Maintenance",
                site_location=f"Site {fake.building_number()}",
                scheduled_date=scheduled,
                hours_required=random.randint(2, 16),
                technician_id=tech.id
            )
            db.add(order)

    db.commit()
    print("Database seeded successfully! Ready for the frontend.")


if __name__ == "__main__":
    seed_database()
    db.close()
