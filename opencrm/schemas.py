from pydantic import BaseModel, Field
from datetime import datetime


class PatientBase(BaseModel):
    name: str
    age: int
    height: int = 0
    weight: int = 0
    blood_group: str
    username: str
    password: str


class Patient(PatientBase):
    id: int

    class Config:
        orm_mode = True


class DoctorBase(BaseModel):
    name: str
    specialization: str
    username: str
    password: str


class Doctor(DoctorBase):
    id: int

    class Config:
        orm_mode = True


class AppointmentBase(BaseModel):
    doctor_id: int
    patient_id: int
    date_time: datetime
    patient_medical_history: str
    patient_medical_summary: str


class Appointment(AppointmentBase):
    id: int

    class Config:
        orm_mode = True


class MedicalHistoryBase(BaseModel):
    patient_id: int
    date: datetime
    disease: str
    medicines: str


class MedicalHistory(MedicalHistoryBase):
    id: int

    class Config:
        orm_mode = True


class PrescriptionBase(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_id: int
    date: datetime
    medicines: str
    precautions: str
    follow_up_date: datetime


class Prescription(PrescriptionBase):
    id: int

    class Config:
        orm_mode = True
