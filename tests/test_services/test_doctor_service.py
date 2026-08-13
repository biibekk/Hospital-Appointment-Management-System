import sqlite3
from unittest import TestCase
from unittest.mock import Mock, patch
from services.doctor_service import DoctorService
from models.doctor_model import DoctorModel

class TestDoctorSerivce(TestCase):
    def setUp(self):
        self.doctor_repo = Mock()
        self.doctor = DoctorModel("demo",1234,"physician",100,1)
        self.doctor_s =  DoctorService(self.doctor_repo)

    def test_add_doctor_already_exists(self):
        self.doctor_s.repo.doctor_exists.return_value = 1

        result_first_if = self.doctor_s.add_doctor(self.doctor) 

        self.doctor_s.repo.doctor_exists.assert_called_once_with(self.doctor)
        self.assertEqual(result_first_if,{'success':False,'message':"Doctor Already Exists."})


    def test_add_doctor_success(self):
        self.doctor_s.repo.doctor_exists.return_value = 0
        self.doctor_s.repo.add_doctor.return_value = 1

        result = self.doctor_s.add_doctor(self.doctor)

        self.doctor_s.repo.doctor_exists.assert_called_once_with(self.doctor)
        self.doctor_s.repo.add_doctor.assert_called_once_with(self.doctor)
        self.assertEqual(result, {'success':True,'message':"Doctor Added Successfully."})

    def test_add_doctor_failed(self):
        self.doctor_s.repo.doctor_exists.return_value = 0
        self.doctor_s.repo.add_doctor.return_value = 0

        result = self.doctor_s.add_doctor(self.doctor)

        self.doctor_s.repo.doctor_exists.assert_called_once_with(self.doctor)
        self.doctor_s.repo.add_doctor.assert_called_once_with(self.doctor)
        self.assertEqual(result,{'success':False,'message':"Failed to Add Doctor."})

    @patch("services.doctor_service.dblogger")
    def test_add_doctor_exception_occurs(self,mocked_dblogger):
        self.doctor_s.repo.doctor_exists.return_value = 0
        self.doctor_s.repo.add_doctor.side_effect = sqlite3.IntegrityError("demo error")

        result = self.doctor_s.add_doctor(self.doctor)

        self.doctor_s.repo.doctor_exists.assert_called_once_with(self.doctor)
        self.doctor_s.repo.add_doctor.assert_called_once_with(self.doctor)
        self.assertEqual(result,{'success': False,'message': "Unable to add doctor schedule. Please try again."})