from fastapi import APIRouter
from opencrm.store import AppointmentStore
from opencrm.database import get_database
from opencrm.utils.utils import get_logger
from opencrm.schemas import Appointment

LOGGER = get_logger(__name__)

router = APIRouter(
    prefix="/appointments",
    tags=["appointments"]
)

db = get_database()

appointment_store = AppointmentStore(
    db
)


@router.post("/")
async def create_appointment(appointment: Appointment):
    appointment_store.create_appointment(appointemnt_details=appointment)
    return {"message": "Appointment created successfully"}


@router.get("/")
async def get_all_appointments():
    return appointment_store.get_all_appointments()


@router.get("/{appointment_id}")
async def get_appointment(appointment_id: int):
    return appointment_store.get_appointment(appointment_id)


@router.get("/patient/{patient_id}")
async def get_appointment_by_patient(patient_id: int):
    return appointment_store.get_appointment_by_patient(patient_id)


@router.get("doctor/{doctor_id}")
async def get_appointment_by_doctor(doctor_id: int):
    return appointment_store.get_appointment_by_doctor(doctor_id)


@router.patch("/{appointment_id}/complete")
async def complete_appointment(appointment_id: int):
    return appointment_store.mark_appointment_attended(appointment_id)
