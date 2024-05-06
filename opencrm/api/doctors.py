from fastapi import APIRouter
from opencrm.store import DoctorStore
from opencrm.database import get_database
from opencrm.schemas import Doctor

router = APIRouter(
    prefix="/doctors",
    tags=["doctor"]
)

db = get_database()

doctor_store = DoctorStore(
    db
)


@router.post("/")
async def create_doctor(doctor: Doctor):
    return doctor_store.create_doctor(doctor)


@router.get("/")
async def get_all_doctors():
    return doctor_store.get_all_doctors()


@router.get("/{doctor_id}")
async def get_doctor_by_id(doctor_id: int):
    return doctor_store.get_doctor(doctor_id)


@router.get("/specialization/{specialization}")
async def get_all_doctors_by_spec(specialization: str):
    return doctor_store.get_doctor_by_specialization(specialization)


@router.get("/{doctor_id}/patients")
async def get_patients(doctor_id: int):
    return doctor_store.get_doctor_patients(doctor_id)


@router.put("/{doctor_id}")
async def update_doctor(doctor_id: int, name: str, specialization: str):
    return doctor_store.update_doctor(doctor_id, name, specialization)

@router.get("/username/{doctor_username}")
async def get_doctor_by_username(doctor_username: str):
    return doctor_store.get_doctor_by_username(doctor_username) 

@router.delete("/{doctor_id}")
async def delete_doctor(doctor_id: int):
    return doctor_store.delete_doctor(doctor_id)