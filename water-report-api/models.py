from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base


class Technician(Base):
    __tablename__ = "technicians"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String)
    region = Column(String)

    # Relationships
    certifications = relationship("Certification", back_populates="technician")
    work_orders = relationship("WorkOrder", back_populates="technician")


class Certification(Base):
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)  # e.g., "Water Treatment Operator Grade II"
    expiry_date = Column(Date)
    is_active = Column(Boolean, default=True)
    technician_id = Column(Integer, ForeignKey("technicians.id"))

    technician = relationship("Technician", back_populates="certifications")


class WorkOrder(Base):
    __tablename__ = "work_orders"

    id = Column(Integer, primary_key=True, index=True)
    task_description = Column(String)
    site_location = Column(String)
    scheduled_date = Column(Date)
    hours_required = Column(Integer)
    technician_id = Column(Integer, ForeignKey("technicians.id"))

    technician = relationship("Technician", back_populates="work_orders")
