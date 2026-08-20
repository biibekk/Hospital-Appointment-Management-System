# python3 -m unittest tests/test_services/test_doctorschedule_service.py

import sqlite3
from unittest import TestCase
from unittest.mock import Mock, patch
from services.doctorschedule_service import DoctorScheduleService

class TestDoctorScheduleService(TestCase):
    def setUp(self):
        self.schedule_repo = Mock()
        self.doctor_repo = Mock()

        self.doctor_s = DoctorScheduleService(self.schedule_repo,self.doctor_repo)


    def test_add_doctor_schedule_doctor_not_found(self):
        schedule = Mock()
        schedule.doctor_id = 1

        self.doctor_s.doctor_repo.doctor_exists.return_value = None

        result = self.doctor_s.add_doctor_schedule(schedule)

        self.doctor_s.doctor_repo.doctor_exists.assert_called_once()
        self.assertEqual(result,{'success':False,'message':"Doctor Not Found."})


    def test_add_doctor_schedule_already_exists(self):
        schedule = Mock()
        schedule.doctor_id = 1

        self.doctor_s.doctor_repo.doctor_exists.return_value = 1
        self.doctor_s.schedule_repo.doctor_schedule_exists.return_value = 1

        result = self.doctor_s.add_doctor_schedule(schedule)

        self.doctor_s.schedule_repo.doctor_schedule_exists.assert_called_once_with(schedule)
        self.assertEqual(result,{'success':False,'message':"Doctor Schedule Already Exists."})


    def test_add_doctor_schedule_success(self):
        schedule = Mock()
        schedule.doctor_id = 1

        self.doctor_s.doctor_repo.doctor_exists.return_value = 1
        self.doctor_s.schedule_repo.doctor_schedule_exists.return_value = None
        self.doctor_s.schedule_repo.add_doctor_schedule.return_value = 1

        result = self.doctor_s.add_doctor_schedule(schedule)

        self.doctor_s.schedule_repo.doctor_schedule_exists.assert_called_once_with(schedule)
        self.doctor_s.schedule_repo.add_doctor_schedule.assert_called_once_with(schedule)
        self.assertEqual(result,{'success':True,'message':"Doctor Schedule Added Successfully."})


    @patch("services.doctorschedule_service.dblogger")
    def test_add_doctor_schedule_error(self,mocked_dblogger):
        schedule = Mock()
        schedule.doctor_id = 1

        self.doctor_s.doctor_repo.doctor_exists.side_effect = sqlite3.Error

        result = self.doctor_s.add_doctor_schedule(schedule)

        mocked_dblogger.error.assert_called_once()
        self.assertEqual(result,{'success': False,'message': "Unable to add doctor schedule. Please try again."})


    def test_get_doctor_slots_success(self):
        doctor_id = 1
        date = "2026-08-21"

        self.doctor_s.schedule_repo.get_doctor_slots.return_value = [(1,"09:00","11:00",30)]

        result = self.doctor_s.get_doctor_slots(doctor_id,date)

        self.doctor_s.schedule_repo.get_doctor_slots.assert_called_once_with(doctor_id,date)
        self.assertEqual(result,[("09:00","09:30"),("09:30","10:00"),("10:00","10:30"),("10:30","11:00")])


    def test_get_doctor_slots_multiple_schedule(self):
        doctor_id = 1
        date = "2026-08-21"

        self.doctor_s.schedule_repo.get_doctor_slots.return_value = [(1,"09:00","10:00",30),(2,"14:00","15:00",30)]

        result = self.doctor_s.get_doctor_slots(doctor_id,date)

        self.doctor_s.schedule_repo.get_doctor_slots.assert_called_once_with(doctor_id,date)
        self.assertEqual(result,[("09:00","09:30"),("09:30","10:00"),("14:00","14:30"),("14:30","15:00")])


    def test_get_doctor_slots_no_slots(self):
        doctor_id = 1
        date = "2026-08-21"

        self.doctor_s.schedule_repo.get_doctor_slots.return_value = []

        result = self.doctor_s.get_doctor_slots(doctor_id,date)

        self.doctor_s.schedule_repo.get_doctor_slots.assert_called_once_with(doctor_id,date)
        self.assertEqual(result,[])


    @patch("services.doctorschedule_service.dblogger")
    def test_get_doctor_slots_error(self,mocked_dblogger):
        doctor_id = 1
        date = "2026-08-21"

        self.doctor_s.schedule_repo.get_doctor_slots.side_effect = sqlite3.Error

        result = self.doctor_s.get_doctor_slots(doctor_id,date)

        mocked_dblogger.error.assert_called_once()
        self.assertEqual(result,{'success': False,'message': "Unable to get doctor slots. Please try again."})