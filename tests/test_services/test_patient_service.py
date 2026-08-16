from unittest import TestCase
from unittest.mock import Mock
from services.patient_service import PatientService
from models.patient_model import PatientModel

class TestPatientService(TestCase):
    def setUp(self):
        self.patient_repo = Mock()
        self.patient = PatientService(self.patient_repo)

    def test_register_patient(self):
        patient = PatientModel(1,"abcd","2004/1/1","male","1234")
        self.patient_repo.patient_exists.return_value = False

        self.patient_repo.register_patient.return_value = 1

        result = self.patient.register_patient(patient)

        self.patient_repo.patient_exists.assert_called_once_with(patient)
        self.patient_repo.register_patient.assert_called_once_with(patient)
        self.assertEqual(result,{'success':True,'message':"Patient Registration Successfully.",'data':patient.patient_id})