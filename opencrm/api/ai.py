import dspy
from fastapi import APIRouter
from opencrm.utils.utils import get_logger
from opencrm.schemas import PatientQuery
from opencrm.ai.modules import patient_details

LOGGER = get_logger(__name__)

router = APIRouter(
    prefix="/ai",
    tags=["ai"]
)


@router.post("/patient")
def predict_patient(patient_queries: PatientQuery):
    vals = patient_details(patient_queries.query, patient_queries.past_diagnosis, patient_queries.past_habits,
                           patient_queries.bmi)
    return vals
