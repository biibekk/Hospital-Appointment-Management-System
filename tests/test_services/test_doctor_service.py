# python3 -m unittest tests/test_services/test_doctor_service.py

import sqlite3
from unittest import TestCase
from unittest.mock import Mock, patch
from services.doctor_service import DoctorService
from models.doctor_model import DoctorModel

class TestDoctorSerivce(TestCase):
    def setUp(self):
        self.doctor_repo = Mock()
        self.doctor = DoctorModel(1,"demo",1234,"physician",100)
        self.doctor_s =  DoctorService(self.doctor_repo)
        # self.doctor_s.doctor_repo = self.doctor_repo

    def test_add_doctor_already_exists(self):
        self.doctor_s.doctor_repo.doctor_exists.return_value = True

        result = self.doctor_s.add_doctor(self.doctor) 

        self.doctor_s.doctor_repo.doctor_exists.assert_called_once_with(self.doctor)
        self.assertEqual(result,{'success':False,'message':"Doctor Already Exists."})


    def test_add_doctor_success(self):
        self.doctor_s.doctor_repo.doctor_exists.return_value = False
        self.doctor_s.doctor_repo.add_doctor.return_value = 1

        result = self.doctor_s.add_doctor(self.doctor)

        self.doctor_s.doctor_repo.doctor_exists.assert_called_once_with(self.doctor)
        self.doctor_s.doctor_repo.add_doctor.assert_called_once_with(self.doctor)
        self.assertEqual(result, {'success':True,'message':"Doctor Added Successfully."})

    def test_add_doctor_failed(self):
        self.doctor_s.doctor_repo.doctor_exists.return_value = False
        self.doctor_s.doctor_repo.add_doctor.return_value = 0

        result = self.doctor_s.add_doctor(self.doctor)

        self.doctor_s.doctor_repo.doctor_exists.assert_called_once_with(self.doctor)
        self.doctor_s.doctor_repo.add_doctor.assert_called_once_with(self.doctor)
        self.assertEqual(result,{'success':False,'message':"Failed to Add Doctor."})

    @patch("services.doctor_service.dblogger")
    def test_add_doctor_exception_occurs(self,mocked_dblogger):
        self.doctor_s.doctor_repo.doctor_exists.return_value = False
        self.doctor_s.doctor_repo.add_doctor.side_effect = sqlite3.IntegrityError("demo error")

        result = self.doctor_s.add_doctor(self.doctor)

        self.doctor_s.doctor_repo.doctor_exists.assert_called_once_with(self.doctor)
        self.doctor_s.doctor_repo.add_doctor.assert_called_once_with(self.doctor)
        mocked_dblogger.error.assert_called_once()
        self.assertEqual(result,{'success': False,'message': "Unable to add doctor schedule. Please try again."})

    def test_get_doctors_from_service_no_doctors(self):
        service = "physician"

        self.doctor_repo.get_doctors_from_service.return_value = []

        result = self.doctor_s.get_doctors_from_service(service)

        self.doctor_s.doctor_repo.get_doctors_from_service.assert_called_once_with(service)
        self.assertEqual(result,{'success':False,'message':f"No doctor added to {service} service."})

    def test_get_doctors_from_service_success(self):
        service = "physician"
        self.doctor_s.doctor_repo.get_doctors_from_service.return_value = [(1,"Dr. John",100),(2,"Dr. Smith",200)]

        result = self.doctor_s.get_doctors_from_service(service)

        self.doctor_s.doctor_repo.get_doctors_from_service.assert_called_once_with(service)
        doctors_data = {1:("Dr. John",100),2:("Dr. Smith",200)}
        doctor_ids = [1,2]
        doctors_choices = (
            "1               Dr. John                  100\n"
            "2               Dr. Smith                 200"
        )
        self.assertEqual(result,{'success':True,'message':f"Doctors with specialisation{service} fetched successfully.",
        'data':(doctors_data,doctor_ids,doctors_choices)})

    @patch("services.doctor_service.dblogger")
    def test_get_doctors_from_service_error(self,mocked_dblogger):
        service = "physician"
        self.doctor_repo.get_doctors_from_service.side_effect = sqlite3.Error

        result = self.doctor_s.get_doctors_from_service(service)

        mocked_dblogger.assert_called_once()
        self.assertEqual(result,{'success':False,'message':f"Unable to fetch doctors with specialisation {service}. Please try again."})