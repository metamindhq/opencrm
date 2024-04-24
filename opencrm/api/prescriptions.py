from fastapi import APIRouter
from opencrm.store import PrescriptionStore
from opencrm.database import get_database
from opencrm.schemas import Prescription

router = APIRouter(
    prefix="/prescriptions",
    tags=["prescriptions"]
)

db = get_database()

prescription_store = PrescriptionStore(
    db
)

@router.post("/")
async def create_prescription(prescription: Prescription, diseases=None):
    if diseases is None:
        diseases = []
    return prescription_store.create_prescription(prescription, diseases=diseases)

@router.get("/{prescription_id}")
async def get_prescription(prescription_id: int):
    return prescription_store.get_prescription(prescription_id)

@router.get("/patient/{patient_id}")
async def get_prescriptions_by_patient(patient_id: int):
    return prescription_store.get_prescriptions_by_patient(patient_id)

@router.get("/doctor/{doctor_id}")
async def get_prescriptions_by_doctor(doctor_id: int):
    return prescription_store.get_prescriptions_by_doctor(doctor_id)

@router.get("/appointment/{appointment_id}")
async def get_prescriptions_by_appointment(appointment_id: int):
    return prescription_store.get_prescriptions_by_appointment(appointment_id)