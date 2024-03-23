from rest_framework.generics import *
from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response as DjangoResponse
from .serializers import *


class GetEvaluations(ListAPIView):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer

class GetDataSets(ListAPIView):
    queryset = TrainingDataSet.objects.all()
    serializer_class = TrainingDataSetSerializer

class GetTestingDataset(ListAPIView):
    queryset = TestingDataSet.objects.all()
    serializer_class = TestingDataSetSerializer


    