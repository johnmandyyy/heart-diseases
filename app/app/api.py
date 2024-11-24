from rest_framework.generics import *
from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response as DjangoResponse
from rest_framework import status
from .serializers import *
from .algorithm import TreeAlgorithm
from datetime import datetime
from .datagen import DataGenerator


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

    def __init__(self):
        self.remarks = False

    def addData(self, data, is_target_true=False):
        get_medicine_id_instance = None

        if is_target_true == True:
            get_medicine_id_instance = Medicines.objects.get(id=data["medicine_id"])

        PatientRecord.objects.create(
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
            self.addData(add_to_record)

            return DjangoResponse(
                {
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
