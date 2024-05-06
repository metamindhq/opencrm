from sqlalchemy.orm import Session
from opencrm.database import do_commit
from opencrm.models import Patient, Appointment, MedicalHistory, Prescription, Doctor
from opencrm.schemas import NewPatient as NewPatientSchema, Patient as PatientSchema, Appointment as AppointmentSchema, \
    MedicalHistory as MedicalHistorySchema, Prescription as PrescriptionSchema, Doctor as DoctorSchema
from datetime import datetime


class PatientsStore:
    def __init__(self, db: Session):
        self.db: Session = db

    def get_patient(self, patient_id):
        res = self.db.query(Patient).filter(Patient.id == patient_id).first()
        return res
    
    def get_patient_by_username(self, patient_username):
        res = self.db.query(Patient).filter(Patient.user_name == patient_username).first()
        return res

    def get_patients(self):
        return self.db.query(Patient).all()

    def get_appointments(self, patient_id: int):
        query = self.db.query(Appointment).filter(Appointment.patient_id == patient_id)
        # sort by date
        return query.order_by(Appointment.date_time).all()

    def get_patient_appointment(self, patient_id: int, appointment_id: int):
        return self.db.query(Appointment).filter(Appointment.patient_id == patient_id,
                                                 Appointment.id == appointment_id).first()

    def get_doc_appointments(self, doctor_id: int):
        return self.db.query(Appointment).filter(Appointment.doctor_id == doctor_id).all()

    def get_medical_history(self, patient_id: int, sort_by_date: bool = False):
        query = self.db.query(MedicalHistory).filter(MedicalHistory.patient_id == patient_id)
        if sort_by_date:
            query = query.order_by(MedicalHistory.date)
        return query.all()

    def get_prescriptions(self, patient_id: int, sort_by_date: bool = False):
        query = self.db.query(Prescription).filter(Prescription.patient_id == patient_id)
        if sort_by_date:
            query = query.order_by(Prescription.date)
        return query.all()

    def get_prescription(self, patient_id: int, prescription_id: int):
        return self.db.query(Prescription).filter(Prescription.patient_id == patient_id,
                                                  Prescription.id == prescription_id).first()

    def create_patient(self, user: NewPatientSchema):
        patient = Patient(name=user.name, age=user.age, height=user.height, weight=user.weight,
                          blood_group=user.blood_group,
                          user_name=user.username, password=user.password)
        query = self.db.add(patient)
        do_commit(self.db)

        if user.medical_history:
            patient = self.get_patient(patient.id)
            self.create_medical_history(
                patient_id=patient.id,
                date=user.medical_history.date,
                disease=user.medical_history.disease,
                medicines=user.medical_history.medicines
            )

        return patient

    def create_medical_history(self, patient_id: int, date: datetime, disease: str, medicines: str):
        medical_history = MedicalHistory(patient_id=patient_id, date=date, disease=disease, medicines=medicines)
        self.db.add(medical_history)
        do_commit(self.db)
        self.db.refresh(medical_history)
        return medical_history

    def create_prescription(self, patient_id: int, doctor_id: int, date: datetime, medicines: str, precautions: str,
                            follow_up_date: datetime):
        prescription = Prescription(patient_id=patient_id, doctor_id=doctor_id, date=date, medicines=medicines,
                                    precautions=precautions, follow_up_date=follow_up_date)
        self.db.add(prescription)
        do_commit(self.db)
        self.db.refresh(prescription)
        return prescription

    def update_patient(self, patient_id: int, patient_details: PatientSchema):
        patient = self.get_patient(patient_id)

        patient.name = patient_details.name
        patient.age = patient_details.age
        patient.height = patient_details.height
        patient.weight = patient_details.weight
        patient.blood_group = patient_details.blood_group
        patient.user_name = patient_details.username
        patient.password = patient_details.password
        do_commit(self.db)
        self.db.refresh(patient)
        return patient


class DoctorStore:
    def __init__(self, db: Session):
        self.db = db

    def get_doctor(self, doctor_id: int):
        # sort by id
        return self.db.query(Doctor).filter(Doctor.id == doctor_id).first()
    

    def get_doctor_by_username(self, doctor_username: str):
        # sort by username
        return self.db.query(Doctor).filter(Doctor.user_name == doctor_username).first()

    def get_all_doctors(self):
        return self.db.query(Doctor).all()

    def get_doctor_by_specialization(self, specialization: str):
        return self.db.query(Doctor).filter(Doctor.specialization == specialization).all()

    def create_doctor(self, doctor: DoctorSchema):
        doctor = Doctor(name=doctor.name, specialization=doctor.specialization, user_name=doctor.username,
                        password=doctor.password)
        self.db.add(doctor)
        do_commit(self.db)
        self.db.refresh(doctor)
        return doctor

    def update_doctor(self, doctor_id: int, name: str, specialization: str):
        doctor = self.get_doctor(doctor_id)
        doctor.name = name
        doctor.specialization = specialization
        do_commit(self.db)
        self.db.refresh(doctor)
        return doctor

    def delete_doctor(self, doctor_id: int):
        doctor = self.get_doctor(doctor_id)
        self.db.delete(doctor)
        do_commit(self.db)
        return doctor

    def get_doctor_patients(self, doctor_id: int):
        return self.db.query(Patient).join(Appointment).filter(Appointment.doctor_id == doctor_id).all()

    def get_doctor_patient(self, doctor_id: int, patient_id: int):
        return self.db.query(Patient).join(Appointment).filter(Appointment.doctor_id == doctor_id,
                                                               Appointment.patient_id == patient_id).first()

    def get_doctor_patient_appointments(self, doctor_id: int, patient_id: int):
        return self.db.query(Appointment).filter(Appointment.doctor_id == doctor_id,
                                                 Appointment.patient_id == patient_id).all()

    def mark_appointment_attended(self, appointment_id: int):
        appointment = self.db.query(Appointment).filter(Appointment.id == appointment_id).first()
        appointment.attended = True
        do_commit(self.db)
        self.db.refresh(appointment)
        return appointment


class AppointmentStore:
    def __init__(self, db: Session):
        self.db = db

    def create_appointment(self, appointemnt_details: AppointmentSchema):
        # Check if same appointement exists between same doctor and patient and unattended
        appointment = self.db.query(Appointment).filter(Appointment.doctor_id == appointemnt_details.doctor_id,
                                                        Appointment.patient_id == appointemnt_details.patient_id,
                                                        Appointment.attended == False).first()
        if appointment:
            raise Exception("Appointment already exists between same doctor and patient and unattended")
        patient_store = PatientsStore(self.db)

        medical_history = patient_store.get_medical_history(appointemnt_details.patient_id)
        # Convert medical history to string and store the interval between each history
        medical_history_str = ""

        if len(medical_history) > 0:
            first = medical_history[0]
            medical_history_str += f"{first.date} - {first.disease} - {first.medicines}\n"
            if len(medical_history) > 1:
                for history in medical_history[2:]:
                    length = (history.date - first.date).days
                    medical_history_str += f"{length} day interval - {history.disease} - {history.medicines}\n"
        else:
            medical_history_str = appointemnt_details.patient_medical_history
                
        appointment = Appointment(doctor_id=appointemnt_details.doctor_id, patient_id=appointemnt_details.patient_id,
                                  date_time=appointemnt_details.date_time,
                                  patient_medical_history=medical_history_str,
                                  patient_medical_summary=appointemnt_details.patient_medical_summary
                                  )
        self.db.add(appointment)
        do_commit(self.db)
        self.db.refresh(appointment)
        return appointment

    def get_appointment(self, appointment_id: int):
        return self.db.query(Appointment).filter(Appointment.id == appointment_id).first()

    def get_all_appointments(self):
        return self.db.query(Appointment).all()

    def get_appointment_by_patient(self, patient_id: int):
        return self.db.query(Appointment).filter(Appointment.patient_id == patient_id).all()

    def get_appointment_by_doctor(self, doctor_id: int):
        return self.db.query(Appointment).filter(Appointment.doctor_id == doctor_id).all()

    def mark_appointment_attended(self, appointment_id: int):
        appointment = self.db.query(Appointment).filter(Appointment.id == appointment_id).first()
        appointment.attended = True
        do_commit(self.db)
        self.db.refresh(appointment)
        return appointment


class MedicalHistoryStore:
    def __init__(self, db: Session):
        self.db = db

    def get_all_medical_history_by_patient_sorted(self, patient_id: int):
        return self.db.query(MedicalHistory).filter(MedicalHistory.patient_id == patient_id).order_by(
            MedicalHistory.date).all()


class PrescriptionStore:
    def __init__(self, db: Session):
        self.db = db

    def create_prescription(self, prescription: PrescriptionSchema, diseases=None):
        if diseases is None:
            diseases = []
        medical_history = MedicalHistory(patient_id=prescription.patient_id, date=prescription.date,
                                         disease=diseases, medicines=prescription.medicines)

        self.db.add(medical_history)
        do_commit(self.db)
        self.db.refresh(medical_history)
        prescription = Prescription(patient_id=prescription.patient_id, doctor_id=prescription.doctor_id,
                                    appointment_id=prescription.appointment_id,
                                    date=prescription.date, medicines=prescription.medicines,
                                    precautions=prescription.precautions, follow_up_date=prescription.follow_up_date)
        self.db.add(prescription)
        do_commit(self.db)
        self.db.refresh(prescription)

        return prescription

    def get_all_prescriptions_by_patient_sorted(self, patient_id: int):
        return self.db.query(Prescription).filter(Prescription.patient_id == patient_id).order_by(
            Prescription.date).all()

    def get_all_prescriptions_by_doctor_sorted(self, doctor_id: int):
        return self.db.query(Prescription).filter(Prescription.doctor_id == doctor_id).order_by(
            Prescription.date).all()

    def get_prescription(self, prescription_id: int):
        return self.db.query(Prescription).filter(Prescription.id == prescription_id).first()

    def get_prescription_by_appointment(self, appointment_id: int):
        return self.db.query(Prescription).filter(Prescription.appointment_id == appointment_id).first()
