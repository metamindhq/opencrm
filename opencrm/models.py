from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from opencrm.database import Base


class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
    password = Column(String, nullable=False)


class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    height = Column(Integer)
    weight = Column(Integer)
    blood_group = Column(String)
    user_name = Column(String, nullable=False)
    password = Column(String, nullable=False)


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"))
    date_time = Column(DateTime, nullable=False)
    patient_medical_history = Column(Text)  # Store patient's medical history (e.g., JSON)
    patient_medical_summary = Column(Text)  # Store patient's medical summary (e.g., JSON)
    attended = Column(Boolean, default=False)


class MedicalHistory(Base):
    __tablename__ = "medical_history"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    date = Column(DateTime, nullable=False)
    disease = Column(String, nullable=False)
    medicines = Column(Text)  # Store prescribed medicines (e.g., JSON)

    patient = relationship("Patient", backref="medical_history")


class Prescription(Base):
    __tablename__ = "prescriptions"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    date = Column(DateTime, nullable=False)
    medicines = Column(Text)  # Store prescribed medicines (e.g., JSON)

    patient = relationship("Patient", backref="prescriptions")
    doctor = relationship("Doctor", backref="prescriptions")
    appointment = relationship("Appointment", backref="prescriptions")

    precautions = Column(Text)  # Store precautions (e.g., JSON)
    follow_up_date = Column(DateTime)  # Store follow-up date
