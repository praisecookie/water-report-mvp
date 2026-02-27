from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
import models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Water Workforce API")

# Allow Next.js frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the database session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "API is live."}


@app.get("/api/compliance-summary")
def get_compliance_summary(db: Session = Depends(get_db)):
    """Calculates how many certifications are active vs. expired."""

    total_certs = db.query(models.Certification).count()
    expired_certs = db.query(models.Certification).filter(
        models.Certification.expiry_date < date.today()
    ).count()

    active_certs = total_certs - expired_certs
    compliance_rate = round((active_certs / total_certs)
                            * 100) if total_certs > 0 else 0

    return {
        "total_certifications": total_certs,
        "active": active_certs,
        "expired": expired_certs,
        "compliance_rate_percentage": compliance_rate
    }


@app.get("/api/technicians")
def get_technicians(db: Session = Depends(get_db)):
    """Fetches all technicians and determines if they are compliant."""
    techs = db.query(models.Technician).all()

    roster = []
    for tech in techs:
        # Get all certs for this specific technician
        certs = db.query(models.Certification).filter(
            models.Certification.technician_id == tech.id
        ).all()

        # Check if any of their certs are expired
        status = "Compliant"
        for cert in certs:
            if cert.expiry_date < date.today():
                status = "Action Required"
                break  # One expired cert makes the whole tech non-compliant

        roster.append({
            "id": tech.id,
            "name": tech.name,
            "role": tech.role,
            "region": tech.region,
            "status": status
        })

    return roster
