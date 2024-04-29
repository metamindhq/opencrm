from typing import Optional
from fastapi import APIRouter
from opencrm.store import PatientsStore
from opencrm.database import get_database
from opencrm.schemas import NewPatient, Patient

router = APIRouter(
    prefix="/patients",
    tags=["patients"]
)

db = get_database()

patients_store = PatientsStore(
    db
)

@router.post("/")
async def create_patient(user: NewPatient):
    return patients_store.create_patient(user=user)


@router.patch("/{patient_id}")
async def update_patient(patient_id: int, user: Patient):
    return patients_store.update_patient(patient_id, patient_details=user)


@router.get("/")
async def get_all_patients():
    return patients_store.get_patients()


@router.get("/{patient_id}")
async def get_patient_by_id(patient_id: int):
    return patients_store.get_patient(patient_id)

@router.get("/username/{patient_username}")
async def get_patient_by_username(patient_username: str):
    return patients_store.get_patient_by_username(patient_username)


@router.get("/{patient_id}/medical_history")
async def get_medical_history(patient_id: int):
    return patients_store.get_medical_history(patient_id, sort_by_date=True)
