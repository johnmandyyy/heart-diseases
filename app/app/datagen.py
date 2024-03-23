import random
from .models import *
class DataGenerator:
    """
    A class for generating dataset for heart diseases.
    """

    medicines = []

    def __init__(self):
        self.__getMedicines()

    def clearExistingData(self):
        TrainingDataSet.objects.all().delete()
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='app_trainingdataset';")

    def getDatasets(self):
        f_list = []
        for instance in TrainingDataSet.objects.all():
            medicine = None
            if instance.medicine_id != None:
                medicine = instance.medicine_id.pk

            instance_data = {
                "id": instance.pk,
                "sex": instance.sex,
                "age": instance.age,
                "cp": instance.cp,
                "trestbps": instance.trestbps,
                "chol": instance.chol,
                "fbs": instance.fbs,
                "thalach": instance.thalach,
                "exang": instance.exang,
                "oldpeak": instance.oldpeak,
                "slope": instance.slope,
                "ca": instance.ca,
                "thal": instance.thal,
                "target": instance.target,
                "medicine_id": medicine,
                "is_healed": instance.is_healed,
            }

            f_list.append(instance_data)

        return f_list

    def generateTrainingData(self):
        #self.clearExistingData()
        self.generateAbnormalRandomData(500)
        self.generateNormalRandomData(500)

    def manualMedicine(self, patient_data):
        medicine_list = self.medicines

        age = patient_data['age']
        trestbps = patient_data['trestbps']
        chol = patient_data['chol']
        fbs = patient_data['fbs']
        thalach = patient_data['thalach']
        exang = patient_data['exang']
        oldpeak = patient_data['oldpeak']
        ca = patient_data['ca']

        # Define conditions for medicine selection based on patient data values
        if age >= 18 and age <= 50:
            if chol > 200:
                return 21
            elif trestbps > 120:
                return 22
            elif fbs:  # If fbs is True
                return 23
            elif thalach < 100:
                return 24
            else:
                return 25
        elif age > 50 and age <= 70:
            if chol > 220:
                return 26
            elif trestbps > 140:
                return 27
            elif exang:  # If exang is True
                return 28
            elif oldpeak > 1.5:
                return 29
            else:
                return 30
        elif age > 70 and age <= 100:
            if chol > 240:
                return 26
            elif trestbps > 160:
                return 27
            elif exang:  # If exang is True
                return 28
            elif oldpeak > 2.0:
                return 29
            else:
                return 30
        else:
            # For age greater than 100, return a default medicine index
            return 30

    def generateNormalRandomData(self, num_samples):
        """
        Create a normal Dataset
        """

        for _ in range(num_samples):

            sex = random.choice([0, 1])
            age = random.randint(18, 100)
            cp = random.choice([0, 1, 2, 3])
            trestbps_mean = 120 + (age - 50) * 0.5 + (sex - 0.5) * 5
            trestbps = random.gauss(trestbps_mean, 15)
            trestbps = max(90, min(trestbps, 200))
            chol_mean = 200 + (age - 50) * 1 + (sex - 0.5) * 5
            chol = random.gauss(chol_mean, 30)
            chol = max(100, min(chol, 400))
            fbs = random.choice([True, False])
            thalach_mean = 220 - age
            thalach = random.gauss(thalach_mean - 20, 25)
            thalach = max(70, min(thalach, 220))
            exang = random.choice([True, False])
            oldpeak = round(random.uniform(0, 4), 1)
            slope = random.choice([0, 1, 2])
            ca = random.randint(0, 3)
            thal = random.choice([1, 2, 3])
            target = random.choice([False])  # Normal heart condition

            medicine_id = self.manualMedicine({
                "age":age, 
                "trestbps":trestbps,
                "chol": chol,
                "fbs": fbs,
                "thalach": thalach,
                "exang": exang,
                "oldpeak": oldpeak,
                "ca": ca
            })

            is_healed = True 

            # Create TrainingDataSet object
            TrainingDataSet.objects.create(
                sex=sex,
                age=age,
                cp=cp,
                trestbps=trestbps,
                chol=chol,
                fbs=fbs,
                thalach=thalach,
                exang=exang,
                oldpeak=oldpeak,
                slope=slope,
                ca=ca,
                thal=thal,
                target=target,
                medicine_id=Medicines.objects.get(id = medicine_id),
                is_healed=is_healed,
            )

            print(f"Generated {num_samples} random TrainingDataSet entries.")
        
    def generateAbnormalRandomData(self, num_samples):
        """
        Create an abnormal Dataset
        """

        for _ in range(num_samples):

            sex = random.choice([0, 1])
            age = random.randint(18, 100)
            cp = random.choice([0, 1, 2, 3])
            trestbps_mean = 120 + (age - 50) * 0.5 + (sex - 0.5) * 5
            trestbps = random.gauss(trestbps_mean, 15)
            trestbps = max(90, min(trestbps, 200))
            chol_mean = 200 + (age - 50) * 1 + (sex - 0.5) * 5
            chol = random.gauss(chol_mean, 30)
            chol = max(100, min(chol, 400))
            fbs = random.choice([True, False])
            thalach_mean = 220 - age
            thalach = random.gauss(thalach_mean - 20, 25)
            thalach = max(70, min(thalach, 220))
            exang = random.choice([True, False])
            oldpeak = round(random.uniform(0, 4), 1)
            slope = random.choice([0, 1, 2])
            ca = random.randint(0, 3)
            thal = random.choice([1, 2, 3])
            target = random.choice([True])

            medicine_id = self.manualMedicine({
                "age":age, 
                "trestbps":trestbps,
                "chol": chol,
                "fbs": fbs,
                "thalach": thalach,
                "exang": exang,
                "oldpeak": oldpeak,
                "ca": ca
            })

            is_healed = True 

            # Create TrainingDataSet object
            TrainingDataSet.objects.create(
                sex=sex,
                age=age,
                cp=cp,
                trestbps=trestbps,
                chol=chol,
                fbs=fbs,
                thalach=thalach,
                exang=exang,
                oldpeak=oldpeak,
                slope=slope,
                ca=ca,
                thal=thal,
                target=target,
                medicine_id=Medicines.objects.get(id=medicine_id),
                is_healed=is_healed,
            )

            print(f"Generated {num_samples} random TrainingDataSet entries.")

    def __getMedicines(self):
        """
        Internal private method
        for getting the medicines using primary key.
        returns a list of primary key.
        """

        self.medicines = []  # Clear medicine list before adding.
        for medicine in Medicines.objects.all():
            self.medicines.append(medicine.id)

        print(self.medicines)

    def generateMedicines(self):
        """
        Generate a dataset for medicines.
        """

        medicines_data = [
            {
                "medicine_name": "Aspirin (Acetylsalicylic Acid)",
                "instruction": "Take one tablet daily with water. Consult your doctor for proper dosage.",
            },
            {
                "medicine_name": "Ibuprofen (Advil, Motrin)",
                "instruction": "Take one tablet with food or milk as needed for pain relief. Do not exceed recommended dosage.",
            },
            {
                "medicine_name": "Naproxen (Aleve)",
                "instruction": "Take one tablet with food and a full glass of water. Do not exceed the recommended dosage or duration of use.",
            },
            {
                "medicine_name": "Omega-3 Fatty Acids",
                "instruction": "Take as directed on the product label, usually with a meal to enhance absorption.",
            },
            {
                "medicine_name": "Coenzyme Q10 (CoQ10)",
                "instruction": "Take with a meal to enhance absorption. Follow the dosage recommended by your doctor.",
            },
            {
                "medicine_name": "Garlic Supplements",
                "instruction": "Take with food to reduce gastrointestinal discomfort. Follow the dosage instructions provided on the label or as recommended by your doctor.",
            },
            {
                "medicine_name": "Magnesium",
                "instruction": "Take with a full glass of water. Follow the dosage recommended by your doctor or as indicated on the product label.",
            },
            {
                "medicine_name": "Vitamin D",
                "instruction": "Take with a meal containing fat to enhance absorption. Follow the dosage recommended by your doctor or as indicated on the product label.",
            },
            {
                "medicine_name": "Hawthorn",
                "instruction": "Take with water or juice. Follow the dosage instructions provided on the label or as recommended by your healthcare provider.",
            },
            {
                "medicine_name": "L-arginine",
                "instruction": "Take on an empty stomach to enhance absorption. Follow the dosage recommended by your doctor or as indicated on the product label.",
            },
        ]

        # Inserting data into the Medicines model
        for medicine_info in medicines_data:
            medicine = Medicines.objects.create(**medicine_info)
            print(f"Added medicine: {medicine.medicine_name}")
