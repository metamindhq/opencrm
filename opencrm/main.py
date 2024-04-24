from fastapi import FastAPI
import os
from opencrm.api.patients import router as patients_router
from opencrm.api.doctors import router as doctors_router
from opencrm.api.appointments import router as appointments_router
from opencrm.api.prescriptions import router as prescriptions_router
from opencrm.utils.utils import get_logger, load_config
from opencrm.database import default_session, engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
LOGGER = get_logger(__name__)
cfg = load_config()
# Add the router to the app
app.include_router(patients_router)
app.include_router(doctors_router)
app.include_router(appointments_router)
app.include_router(prescriptions_router)


@app.get("/")
async def root():
    # Return system information
    return {
    "version": "0.1",
    "name": "OpenCRM",
    "status": "running",
    "config": cfg,
    "system": {
        "CPU": os.cpu_count(),
        "memory": os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES'),
        "disk": os.statvfs('/').f_frsize * os.statvfs('/').f_blocks,
        "os": os.uname()
    }
    }
