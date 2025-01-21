from django.db import models
from app.models import *
from datetime import date
from app.models import Patients

class GetPatient:

    def __init__(self):
        pass

    def get_patient_count(self):
        patient_count = Patients.objects.all()
        return len(patient_count)
        


class GetPrescription:

    prescription_id = None

    __formatted_data = {
        "patient_first_name": "",
        "patient_last_name": "",
        "patient_age": "",
        "patient_sex": "",
        "patient_address": "",
        "physician_signature": "",
        "physician_license_no": "",
        "physician_notes": "",
        "physician_description": "",
        "date_recorded": "",
    }

    def __init__(self, id: int):
        self.prescription_id = id
        self.__get_data()

    def __get_data(self):
        """Get prescription data using ORM."""
        try:

            result = Prescription.objects.all().filter(id=self.prescription_id)

            if len(result) > 0:
                today = date.today()
                for patient in result:

                    birth_date = patient.patiend_record_id.patient_id.birth_date

                    self.__formatted_data = {
                        "patient_first_name": patient.patiend_record_id.patient_id.name,
                        "patient_middle_name": patient.patiend_record_id.patient_id.middle_name,
                        "patient_last_name": patient.patiend_record_id.patient_id.last_name,
                        "patient_age": today.year
                        - birth_date.year
                        - (
                            (today.month, today.day)
                            < (birth_date.month, birth_date.day)
                        ),
                        "patient_sex": (
                            "Male"
                            if patient.patiend_record_id.patient_id.sex == 0
                            else "Female"
                        ),
                        "patient_address": "",
                        "phyisician_name": (
                            patient.physician.physician_account.first_name
                            + " "
                            + patient.physician.physician_account.last_name
                            + " "
                            + patient.physician.suffixes
                        ),
                        "physician_signature": "/media/"
                        + str(patient.physician.e_signature),
                        "physician_license_no": str(patient.physician.license_no),
                        "physician_notes": str(patient.notes),
                        "physician_description": str(patient.description),
                        "date_recorded": str(patient.date_recorded),
                    }

                    break

        except Exception as e:
            print(e)

    def retrieve_prescription_record(self):
        return self.__formatted_data
