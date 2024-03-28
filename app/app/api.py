from rest_framework.generics import *
from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response as DjangoResponse
from rest_framework import status
from .serializers import *
from .algorithm import TreeAlgorithm


class DiagnoseDisease(APIView):

    def __init__(self):
        self.remarks = False

    def post(self, request, format = None):
        
        # Predict if normal or not.

        Predictor = TreeAlgorithm()
        result = Predictor.loadModelAndPredict(request.data)
        
        if result[0] == True:

        # Predict if normal or not.

            result = Predictor.loadModelAndPredictMedicine(request.data)
            instance = Medicines.objects.get(id = result[0])
            print(instance.medicine_name, instance.instruction)

            return DjangoResponse({
                    "remarks": True,
                    "message": f'{instance.medicine_name}' + " : " + f'{instance.instruction}'
                }, status = status.HTTP_200_OK
            )

        else:

            return DjangoResponse({
                    "remarks": False,
                    "message": "Patient is normal."
                }, status = status.HTTP_200_OK
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


    