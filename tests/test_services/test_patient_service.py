# python3 -m unittest tests/test_services/test_patient_service.py
import sqlite3
from unittest import TestCase
from unittest.mock import Mock,patch
from services.patient_service import PatientService
from models.patient_model import PatientModel

class TestPatientService(TestCase):
    def setUp(self):
        self.patient_repo = Mock()
        self.patient_s = PatientService(self.patient_repo)

    def test_patient_exists_true(self):
        patient = PatientModel(1,"abcd","2004/1/1","male","1234")
        self.patient_s.patient_repo.patient_exists.return_value = 1

        result = self.patient_s.patient_exists(patient)

        self.patient_s.patient_repo.patient_exists.assert_called_once_with(patient)
        self.assertEqual(result,{'success': True,'message': f"Patient Account Already exists with ID {patient.patient_id}"})


    def test_patient_exists_false(self):
        patient = PatientModel(1,"abcd","2004/1/1","male","1234")
        self.patient_s.patient_repo.patient_exists.return_value = None

        result = self.patient_s.patient_exists(patient)

        self.patient_s.patient_repo.patient_exists.assert_called_once_with(patient)
        self.assertEqual(result,{'success': False,'message': f"Patient with id {patient.patient_id} Not Found"})


    @patch("services.patient_service.dblogger")
    def test_patient_exists_error(self,mocked_dblogger):
        patient = PatientModel(1,"abcd","2004/1/1","male","1234")
        self.patient_s.patient_repo.patient_exists.side_effect = sqlite3.Error

        result = self.patient_s.patient_exists(patient)

        self.patient_s.patient_repo.patient_exists.assert_called_once_with(patient)
        mocked_dblogger.error.assert_called_once()
        self.assertEqual(result,{'success': False,'message': "Unable to check if patient exists. Please try again."})


    @patch("services.patient_service.PatientService.patient_exists")
    def test_register_patient_success(self,mocked_patient_exists):
        patient = PatientModel(1,"abcd","2004/1/1","male","1234")
        mocked_patient_exists.return_value = {'success': False,'message': f"Patient with id {patient.patient_id} Not Found"}
        # real class method patient_exists is called, so patch

        self.patient_s.patient_repo.register_patient.return_value = 1

        result = self.patient_s.register_patient(patient)

        mocked_patient_exists.assert_called_once_with(patient)
        self.patient_s.patient_repo.register_patient.assert_called_once_with(patient)
        self.assertEqual(result,{'success':True,'message':"Patient Registration Successfully.",'data':patient.patient_id})


    @patch("services.patient_service.PatientService.patient_exists")
    def test_register_patient_fails(self,mocked_patient_exists):
        patient = PatientModel(1,"abcd","2004/1/1","male","1234")
        mocked_patient_exists.return_value = {'success': True,'message': f"Patient Account Already exists with ID {patient.patient_id}"}

        result = self.patient_s.register_patient(patient)
        mocked_patient_exists.assert_called_once_with(patient)
        self.assertEqual(result,{'success':False,'message':f"Patient Account Already exists with ID {patient.patient_id}"})


    @patch("services.patient_service.dblogger")
    @patch("services.patient_service.PatientService.patient_exists")
    def test_register_patient_error(self,mocked_patient_exists,mocked_dblogger):
        patient = PatientModel(1,"abcd","2004/1/1","male","1234")
        mocked_patient_exists.side_effect = sqlite3.Error

        result = self.patient_s.register_patient(patient)

        mocked_patient_exists.assert_called_once_with(patient)
        mocked_dblogger.error.assert_called_once()
        self.assertEqual(result,{'success': False,'message': "Unable to register patient. Please try again."})


    def test_get_patient_info_found(self):
        patient = PatientModel(1,"abcd","2004/1/1","male","1234")
        self.patient_s.patient_repo.get_patient_info.return_value = patient

        result = self.patient_s.get_patient_info(patient.patient_id)

        self.patient_s.patient_repo.get_patient_info.assert_called_once_with(patient.patient_id)
        self.assertEqual(result,{'success':True,'message':"Patient information fetched successfully.",'data':patient})


    def test_get_patient_info_not_found(self):
        patient = PatientModel(1,"abcd","2004/1/1","male","1234")
        self.patient_s.patient_repo.get_patient_info.return_value = None

        result = self.patient_s.get_patient_info(patient.patient_id)

        self.patient_s.patient_repo.get_patient_info.assert_called_once_with(patient.patient_id)
        self.assertEqual(result,{'success':False,'message':f"Patient with ID {patient.patient_id} Not Found."})


    @patch("services.patient_service.dblogger")
    def test_get_patient_info_error(self,mocked_dblogger):
        patient_id = 1
        self.patient_repo.get_patient_info.side_effect = sqlite3.Error

        result = self.patient_s.get_patient_info(patient_id)

        mocked_dblogger.error.assert_called_once()
        self.assertEqual(result,{'success': False,'message': "Unable to fetch patient information. Please try again."})
