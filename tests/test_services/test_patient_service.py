from unittest import TestCase
from unittest.mock import Mock,patch
from services.patient_service import PatientService
from models.patient_model import PatientModel

class TestPatientService(TestCase):
    def setUp(self):
        self.patient_repo = Mock()
        self.patient = PatientService(self.patient_repo)

    @patch("services.patient_service.PatientService.patient_exists")
    def test_register_patient(self,mocked_patient_exists):
        patient = PatientModel(1,"abcd","2004/1/1","male","1234")
        mocked_patient_exists.return_value = {'success': False,'message': "Patient Not Found"}
        # real class method patient_exists is called, so patch

        self.patient_repo.register_patient.return_value = 1

        result = self.patient.register_patient(patient)

        self.patient_repo.register_patient.assert_called_once_with(patient)
        self.assertEqual(result,{'success':True,'message':"Patient Registration Successfully.",'data':patient.patient_id})