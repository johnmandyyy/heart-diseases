from rest_framework.generics import *
from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response as DjangoResponse
from rest_framework import status
from .serializers import *
from .algorithm import TreeAlgorithm
from datetime import datetime
from .datagen import DataGenerator
from datetime import date
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from app.models import Prescription
from django.contrib.auth.models import User
from django.contrib import messages
from app.models import Cardiologists

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = "__all__"


class PatientPrescription(APIView):

    def get_patient_records(self, patient_id):
        files = []
        records = (
            PatientRecord.objects.all().filter(patient_id=patient_id).order_by("-id")
        )

        if len(records) > 0:
            for record in records:
                has_prescription = self.get_prescription_records(record.pk)
                files.append(
                    {
                        "patient_id": record.patient_id.pk,
                        "sex": record.sex,
                        "age": record.age,
                        "cp": record.cp,
                        "trestbps": record.trestbps,
                        "chol": record.chol,
                        "fbs": record.fbs,
                        "thalach": record.thalach,
                        "exang": record.exang,
                        "oldpeak": record.oldpeak,
                        "slope": record.slope,
                        "ca": record.ca,
                        "thal": record.thal,
                        "target": record.target,
                        "medicine_id": record.medicine_id,
                        "is_healed": record.is_healed,
                        "date_recorded": str(record.date_recorded),
                        "prescription": {
                            "has_prescription": has_prescription is not None,
                            "prescription_id": (
                                None if has_prescription is None else has_prescription
                            ),
                        },
                    }
                )

        return files

    def get_prescription_records(self, record_id):

        records = (
            Prescription.objects.all()
            .filter(patiend_record_id=record_id)
            .order_by("-id")
        )

        if len(records) > 0:
            for record in records:
                return record.pk

        return None

    def get_patients(self):
        patients = Patients.objects.all().order_by("last_name")
        records = []

        if len(patients) > 0:
            for patient in patients:
                recs = self.get_patient_records(patient.pk)
                print(recs)
                records.append(
                    {
                        "patient": str(patient.last_name) + ", " + str(patient.name) + " " + str(patient.middle_name),
                        "diagnosis": recs,
                    }
                )

        return records

    def get(self, request):
        records = self.get_patients()
        print(records)
        return DjangoResponse({"data": records}, 200)


class UpdatePrescription(RetrieveUpdateDestroyAPIView):

    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer


class GetPrescription(APIView):

    def __init__(self):
        pass


class GenerateRandomDataSet(APIView):

    def __init__(self):
        pass

    def post(self, request, format=None):
        try:

            serializer = GenerateDataSetSerializer(data=request.data)
            if serializer.is_valid() == True:

                if request.data["is_generate"] == True:

                    D = DataGenerator()
                    D.clearExistingData()
                    D.generateTrainingData()

                    return DjangoResponse(
                        {"message": "Adding of random data was done."},
                        status.HTTP_201_ACCEPTED,
                    )

                return DjangoResponse(
                    {"message": "Nothing was trained"}, status.HTTP_202_ACCEPTED
                )

            else:

                return DjangoResponse(
                    {"message": "Invalid request."}, status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:

            return DjangoResponse(
                {"message": "An error occured: " + str(e)},
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TrainHeartDataSet(APIView):

    def __init__(self):
        pass

    def post(self, request, format=None):
        try:

            serializer = TrainHeartDataSetSerializer(data=request.data)
            if serializer.is_valid() == True:
                if request.data["is_train"] == True:

                    Tree = TreeAlgorithm()
                    Tree.adaBoost()

                    return DjangoResponse(
                        {"message": "Training was done."}, status.HTTP_200_OK
                    )
                return DjangoResponse(
                    {"message": "Nothing was trained."}, status.HTTP_202_ACCEPTED
                )

            else:

                return DjangoResponse(
                    {"message": "Invalid request."}, status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:

            return DjangoResponse(
                {"message": "An error occured: " + str(e)},
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DiagnoseDisease(APIView):

    @csrf_exempt
    def __init__(self):
        self.remarks = False

    @csrf_exempt
    def addData(self, data, is_target_true=False):
        get_medicine_id_instance = None

        # If is_target_true is True, get the associated Medicine instance
        if is_target_true:
            get_medicine_id_instance = Medicines.objects.get(id=data["medicine_id"])

        # Create the new PatientRecord instance
        patient_record = PatientRecord.objects.create(
            patient_id=Patients.objects.get(id=data["id"]),
            sex=data["sex"],
            age=data["age"],
            cp=data["cp"],
            trestbps=data["trestbps"],
            chol=data["chol"],
            fbs=data["fbs"],
            thalach=data["thalach"],
            exang=data["exang"],
            oldpeak=data["oldpeak"],
            slope=data["slope"],
            ca=data["ca"],
            thal=data["thal"],
            target=data["target"],
            medicine_id=get_medicine_id_instance,
            date_recorded=datetime.now().strftime("%Y-%m-%d"),
        )

        # import pdb
        # pdb.set_trace()
        return patient_record.id

    @csrf_exempt
    def create_prescription(self, request, data):

        try:

            physician_in_charge = Cardiologists.objects.get(
                    physician_account = User.objects.get(id=request.user.pk)
                )

            # import pdb
            # pdb.set_trace()
                
            Prescription.objects.create(
                patiend_record_id=PatientRecord.objects.get(id=data["patient_id"]),
                date_recorded=date.today(),
                notes="",
                description=data["description"],
                physician = physician_in_charge,
            )

        except Exception as e:
            print(e, "There is a problem in creating.")

    @csrf_exempt
    def post(self, request, format=None):

        Predictor = TreeAlgorithm()
        result_of_target = Predictor.loadModelAndPredict(request.data)

        if result_of_target[0] == True:

            result_of_medicine = Predictor.loadModelAndPredictMedicine(request.data)
            print(result_of_medicine)
            instance = Medicines.objects.get(id=result_of_medicine[0])
            print(instance.medicine_name, instance.instruction)

            add_to_record = request.data  # Assign data to add_record

            # Add more values
            add_to_record.update({"target": result_of_target[0]})
            add_to_record.update({"medicine_id": result_of_medicine[0]})

            patient_record_id = self.addData(add_to_record)

            data = {
                "patient_id": patient_record_id,
                "notes": "",
                "description": f"{instance.medicine_name}"
                + " : "
                + f"{instance.instruction}",
            }

            self.create_prescription(request, data)

            # Return the primary key (id) of the created PatientRecord
            result = Prescription.objects.all().filter(
                patiend_record_id = patient_record_id
            )

            # import pdb
            # pdb.set_trace()

            prescription_id = None
            for record in result:
                prescription_id = record.pk
                break

            return DjangoResponse(
                {
                    "patient_record_id": prescription_id,
                    "remarks": True,
                    "message": f"{instance.medicine_name}"
                    + " : "
                    + f"{instance.instruction}",
                },
                status=status.HTTP_200_OK,
            )

        else:

            add_to_record = request.data  # Assign data to add_record

            # Add more values
            add_to_record.update({"target": False})

            add_to_record.update({"medicine_id": None})

            self.addData(add_to_record, False)

            return DjangoResponse(
                {"remarks": False, "message": "Patient is normal."},
                status=status.HTTP_200_OK,
            )


class CardioInfo(APIView):

    def __init__(self):
        pass

    def __get_cardiologist(self, request):
        data = {}
        user_instance = User.objects.get(id = request.user.pk)
        cardio = Cardiologists.objects.all().filter(
            physician_account = user_instance
            )

        if len(cardio) > 0:
            for user in cardio:
                data = {
                    'first_name': user_instance.first_name,
                    'last_name': user_instance.last_name,
                    'suffixes': user.suffixes,
                    'license_no': user.license_no,
                    'e_signature': str(user.e_signature)
                }

        return data
        
    def get(self, request):
        data = self.__get_cardiologist(request)                
        return DjangoResponse(data, 200)

    def patch(self, request):

        user_instance = User.objects.get(id=request.user.pk)
        cardio = Cardiologists.objects.filter(physician_account=user_instance)

        if not cardio.exists():
            return DjangoResponse({'detail': 'Cardiologist not found for this user.'}, status=status.HTTP_404_NOT_FOUND)

        cardio = cardio.first()

        # Extracting data from the request
        suffixes = request.data['suffixes']
        license_no = request.data['license_no']
        e_signature = request.data['e_signature']

        # Update fields if they are provided in the request
        if suffixes:
            cardio.suffixes = suffixes
        if license_no:
            cardio.license_no = license_no
        if e_signature:
            cardio.e_signature = e_signature

        # Save the updated cardiologist instance
        cardio.save()

        # Return the updated data
        return DjangoResponse({
            'first_name': user_instance.first_name,
            'last_name': user_instance.last_name,
            'suffixes': cardio.suffixes,
            'license_no': cardio.license_no,
            'e_signature': str(cardio.e_signature)
        }, status=status.HTTP_200_OK)

class CreateAccount(APIView):

    def __init__(self):
        pass
    
    def __update_account(self, request):

        if request.data['is_active'] == True:

            try:

                user = User.objects.all().filter(id = request.data['id'])

                if len(user) > 0:

                    user.update(is_active = True)
                    user_instance = User.objects.get(id = request.data['id'])

                    if user_instance.is_staff == True:

                        Cardiologists.objects.create(
                            physician_account = user_instance
                        )

                    else:
                        user.update(is_superuser = True)

                    return True

            except Exception as e:
                return False

        else:

            try:
                user = User.objects.all().filter(id = request.data['id'])
                if len(user) > 0:
                    user.delete()
                    return True
            except Exception as e:
                return False
        
        return False

    def __create_account(self, request):
        
        data = {

            'first_name': request.data['first_name'],
            'username': request.data['username'],
            'password': request.data['password'],
            'last_name': request.data['last_name'],
            'email': request.data['email'],
            'is_staff': request.data['is_staff'],
            'is_active': False
            
        }
        
        user = User.objects.create_user(username=data['username'], 
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            is_staff=data['is_staff'],
            is_active=data['is_active'])

    def patch(self, request):
        try:

            is_updated = self.__update_account(request)
            return DjangoResponse({
                "message": "Updated" if is_updated == True else "Not updated."
            }, 202)

        except Exception as e:

            return DjangoResponse({
                "message": str(e)
            }, 400)

    def post(self, request):
        try:

            self.__create_account(request)
            return DjangoResponse({
                "message": "Account Created"
            }, 201)

        except Exception as e:
            return DjangoResponse({
                "message": str(e)
            }, 400)


    def __get_pending_accounts(self, request):
        pending_accounts = []
        pending = User.objects.all().filter(is_active = False)
        if len(pending) > 0:
            for each in pending:
                pending_accounts.append(
                    {
                        "id": each.pk,
                        "first_name": each.first_name,
                        "last_name": each.last_name,
                        "email": each.email,
                        "is_active": False,
                        "is_staff": each.is_staff
                    }
                )

        return pending_accounts

    def get(self, request):
        """Gets pending account."""
        accounts = self.__get_pending_accounts(request)
        return DjangoResponse({
                        "message": "Goods.",
                        "data": accounts
                    }, 200)


class GetEvaluations(ListAPIView):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer


class GetDataSets(ListAPIView):
    queryset = TrainingDataSet.objects.all()
    serializer_class = TrainingDataSetSerializer


class GetTestingDataset(ListAPIView):
    queryset = TestingDataSet.objects.all()
    serializer_class = TestingDataSetSerializer


class AddPatients(ListCreateAPIView):
    queryset = Patients.objects.all()
    serializer_class = PatientsSerializer
