# python3 -m unittest tests/test_services/test_appointments_service.py

import sqlite3
from unittest import TestCase
from unittest.mock import Mock,patch
from services.appointments_service import AppointmentsService
from models.appointments_model import AppointmentsModel


class TestAppointmentsService(TestCase):
    def setUp(self):
        self.appo_repo = Mock()
        self.doctor_repo = Mock()
        self.doc_sched_s = Mock()
        self.doctor_s = Mock()

        self.appointment_s = AppointmentsService(
            self.appo_repo,
            self.doctor_repo,
            self.doc_sched_s,
            self.doctor_s
        )


    def test_get_booked_doctor_slots_success(self):
        doctor_id = 1
        date = "2026-08-20"
        self.appointment_s.appo_repo.get_booked_doctor_slots.return_value = [("09:00","09:30"),("10:00","10:30")]

        result = self.appointment_s.get_booked_doctor_slots(doctor_id,date)

        self.appointment_s.appo_repo.get_booked_doctor_slots.assert_called_once_with(doctor_id,date)
        self.assertEqual(result,[("09:00","09:30"),("10:00","10:30")])


    @patch("services.appointments_service.dblogger")
    def test_get_booked_doctor_slots_error(self,mocked_dblogger):
        doctor_id = 1
        date = "2026-08-20"
        self.appointment_s.appo_repo.get_booked_doctor_slots.side_effect = sqlite3.Error

        result = self.appointment_s.get_booked_doctor_slots(doctor_id,date)

        mocked_dblogger.error.assert_called_once()
        self.assertEqual(result,{'success': False,'message': f"Unable to fetch booked slots for doctor id {doctor_id}. Please try again."})


    def test_get_doctors_free_slots_success(self):
        doctor_day_slots = [("09:00","09:30"),("10:00","10:30"),("11:00","11:30")]
        doctor_id = 1
        date = "2026-08-20"

        self.appointment_s.appo_repo.get_booked_doctor_slots.return_value = [("10:00","10:30")]

        result = self.appointment_s.get_doctors_free_slots(doctor_day_slots,doctor_id,date)

        self.appointment_s.appo_repo.get_booked_doctor_slots.assert_called_once_with(doctor_id,date)
        self.assertEqual(result[0],[("09:00","09:30"),("11:00","11:30")])


    @patch("services.appointments_service.dblogger")
    def test_get_doctors_free_slots_error(self,mocked_dblogger):
        doctor_day_slots = [("09:00","09:30")]
        doctor_id = 1
        date = "2026-08-20"

        self.appointment_s.appo_repo.get_booked_doctor_slots.side_effect = sqlite3.Error

        result = self.appointment_s.get_doctors_free_slots(doctor_day_slots,doctor_id,date)

        mocked_dblogger.error.assert_called_once()
        self.assertEqual(result,{'success': False,'message': "Unable to get doctors free slot. Please try again."})


    def test_book_appointment_success(self):
        appointment = Mock()
        self.appointment_s.appo_repo.check_patient_appointment_overlap.return_value = None
        self.appointment_s.appo_repo.book_appointment.return_value = 10

        result = self.appointment_s.book_appointment(appointment)

        self.appointment_s.appo_repo.check_patient_appointment_overlap.assert_called_once_with(appointment)
        self.appointment_s.appo_repo.book_appointment.assert_called_once_with(appointment)
        self.assertEqual(result,{'success':True,'message':"Appointment Booked Successfully.",'data':10})


    def test_book_appointment_overlap(self):
        appointment = Mock()
        self.appointment_s.appo_repo.check_patient_appointment_overlap.return_value = appointment

        result = self.appointment_s.book_appointment(appointment)

        self.appointment_s.appo_repo.check_patient_appointment_overlap.assert_called_once_with(appointment)
        self.assertEqual(result,{'success': False,'message': "Another appointment exists for same time.",'data': appointment})


    @patch("services.appointments_service.dblogger")
    def test_book_appointment_error(self,mocked_dblogger):
        appointment = Mock()
        self.appointment_s.appo_repo.check_patient_appointment_overlap.side_effect = sqlite3.Error

        result = self.appointment_s.book_appointment(appointment)

        mocked_dblogger.error.assert_called_once()
        self.assertEqual(result,{'success': False,'message': "Unable to book appointment. Please try again."})


    def test_cancel_appointment_success(self):
        appointment_id = 1
        self.appointment_s.appo_repo.cancel_appointment.return_value = 1

        result = self.appointment_s.cancel_appointment(appointment_id)

        self.appointment_s.appo_repo.cancel_appointment.assert_called_once_with(appointment_id)
        self.assertEqual(result,{'success':True,'message':"Appointment Cancelled Successfully."})


    def test_cancel_appointment_not_found(self):
        appointment_id = 1
        self.appointment_s.appo_repo.cancel_appointment.return_value = None

        result = self.appointment_s.cancel_appointment(appointment_id)

        self.appointment_s.appo_repo.cancel_appointment.assert_called_once_with(appointment_id)
        self.assertEqual(result,{'success':False,'message':f"Appointment with ID {appointment_id} doesn't exists."})


    @patch("services.appointments_service.dblogger")
    def test_cancel_appointment_error(self,mocked_dblogger):
        appointment_id = 1
        self.appointment_s.appo_repo.cancel_appointment.side_effect = sqlite3.Error

        result = self.appointment_s.cancel_appointment(appointment_id)

        mocked_dblogger.error.assert_called_once()
        self.assertEqual(result,{'success': False,'message': "Unable to cancel appointment. Please try again."})


    def test_get_appointment_details_found(self):
        appointment_id = 1
        appointment = Mock()
        self.appointment_s.appo_repo.get_appointment_details.return_value = appointment

        result = self.appointment_s.get_appointment_details(appointment_id)

        self.appointment_s.appo_repo.get_appointment_details.assert_called_once_with(appointment_id)
        self.assertEqual(result,{'success':True,'message':"Appointment Details Fetched Successfully.",'data':appointment})


    def test_get_appointment_details_not_found(self):
        appointment_id = 1
        self.appointment_s.appo_repo.get_appointment_details.return_value = None

        result = self.appointment_s.get_appointment_details(appointment_id)

        self.appointment_s.appo_repo.get_appointment_details.assert_called_once_with(appointment_id)
        self.assertEqual(result,{'success':False,'message':f"Appointment with ID {appointment_id} doesn't exists."})


    @patch("services.appointments_service.dblogger")
    def test_get_appointment_details_error(self,mocked_dblogger):
        appointment_id = 1
        self.appointment_s.appo_repo.get_appointment_details.side_effect = sqlite3.Error

        result = self.appointment_s.get_appointment_details(appointment_id)

        mocked_dblogger.error.assert_called_once()
        self.assertEqual(result,{'success': False,'message': "Unable to fetch appointment details. Please try again."})


    def test_reschedule_appointment_success(self):
        appointment_id = 1
        date = "2026-08-20"
        start_time = "09:00"
        end_time = "09:30"

        self.appointment_s.appo_repo.reschedule_appointment.return_value = 1

        result = self.appointment_s.reschedule_appointment(date,start_time,end_time,appointment_id)

        self.appointment_s.appo_repo.reschedule_appointment.assert_called_once_with(date,start_time,end_time,appointment_id)
        self.assertEqual(result,{'success':True,'message':"Appointment Rescheduled Successfully."})


    @patch("services.appointments_service.dblogger")
    def test_reschedule_appointment_error(self,mocked_dblogger):
        appointment_id = 1
        date = "2026-08-20"
        start_time = "09:00"
        end_time = "09:30"

        self.appointment_s.appo_repo.reschedule_appointment.side_effect = sqlite3.Error

        result = self.appointment_s.reschedule_appointment(date,start_time,end_time,appointment_id)

        mocked_dblogger.error.assert_called_once()
        self.assertEqual(result,{'success': False,'message': "Unable to reschedule appointment. Please try again."})


    def test_view_appointment_history_found(self):
        patient_id = 1
        appointments = [Mock(),Mock()]
        self.appointment_s.appo_repo.view_appointment_history.return_value = appointments

        result = self.appointment_s.view_appointment_history(patient_id)

        self.appointment_s.appo_repo.view_appointment_history.assert_called_once_with(patient_id)
        self.assertEqual(result,{'success':True,'message':"Appointments history fetched successfully.",'data':appointments})


    def test_view_appointment_history_not_found(self):
        patient_id = 1
        self.appointment_s.appo_repo.view_appointment_history.return_value = None

        result = self.appointment_s.view_appointment_history(patient_id)

        self.appointment_s.appo_repo.view_appointment_history.assert_called_once_with(patient_id)
        self.assertEqual(result,{'success':False,'message':f"No Appointments exists for patient {patient_id}.",'data':None})


    @patch("services.appointments_service.dblogger")
    def test_view_appointment_history_error(self,mocked_dblogger):
        patient_id = 1
        self.appointment_s.appo_repo.view_appointment_history.side_effect = sqlite3.Error

        result = self.appointment_s.view_appointment_history(patient_id)

        mocked_dblogger.error.assert_called_once()
        self.assertEqual(result,{'success': False,'message': "Unable to fetch appointments history. Please try again."})


    def test_get_doctor_appointments_today_doctor_not_found(self):
        doctor_id = 1
        date = "2026-08-20"
        self.appointment_s.doctor_repo.doctor_exists.return_value = None

        result = self.appointment_s.get_doctor_appointments_today(doctor_id,date)

        self.appointment_s.doctor_repo.doctor_exists.assert_called_once()
        self.assertEqual(result,{'success':False,'message':f"Doctor with ID {doctor_id} not found."})


    def test_get_doctor_appointments_today_found(self):
        doctor_id = 1
        date = "2026-08-20"
        appointments = [Mock(),Mock()]

        self.appointment_s.doctor_repo.doctor_exists.return_value = 1
        self.appointment_s.appo_repo.get_doctor_appointments_today.return_value = appointments

        result = self.appointment_s.get_doctor_appointments_today(doctor_id,date)

        self.appointment_s.doctor_repo.doctor_exists.assert_called_once()
        self.appointment_s.appo_repo.get_doctor_appointments_today.assert_called_once_with(doctor_id,date)
        self.assertEqual(result,{'success':True,'message':"Today's Appointments fetched successfully,",'data':appointments})


    def test_get_doctor_appointments_today_not_found(self):
        doctor_id = 1
        date = "2026-08-20"

        self.appointment_s.doctor_repo.doctor_exists.return_value = 1
        self.appointment_s.appo_repo.get_doctor_appointments_today.return_value = None

        result = self.appointment_s.get_doctor_appointments_today(doctor_id,date)

        self.appointment_s.appo_repo.get_doctor_appointments_today.assert_called_once_with(doctor_id,date)
        self.assertEqual(result,{'success':False,'message':f"No Appointments today for doctor {doctor_id}.",'data':None})


    @patch("services.appointments_service.dblogger")
    def test_get_doctor_appointments_today_error(self,mocked_dblogger):
        doctor_id = 1
        date = "2026-08-20"

        self.appointment_s.doctor_repo.doctor_exists.side_effect = sqlite3.Error

        result = self.appointment_s.get_doctor_appointments_today(doctor_id,date)

        mocked_dblogger.error.assert_called_once()
        self.assertEqual(result,{'success': False,'message': "Unable to fetch today's appointments. Please try again."})


    def test_get_normal_appointment_not_found(self):
        doctor_id = 1
        date = "2026-08-20"
        start_time = "09:00"
        end_time = "09:30"

        self.appointment_s.appo_repo.get_normal_appointment.return_value = None

        result = self.appointment_s.get_normal_appointment(doctor_id,date,start_time,end_time)

        self.appointment_s.appo_repo.get_normal_appointment.assert_called_once_with(doctor_id,date,start_time)
        self.assertEqual(result,{'success':False,'message':"Normal Appointmens not found."})


    @patch("services.appointments_service.dblogger")
    def test_get_normal_appointment_error(self,mocked_dblogger):
        doctor_id = 1
        date = "2026-08-20"
        start_time = "09:00"
        end_time = "09:30"

        self.appointment_s.appo_repo.get_normal_appointment.side_effect = sqlite3.Error

        result = self.appointment_s.get_normal_appointment(doctor_id,date,start_time,end_time)

        mocked_dblogger.error.assert_called_once()
        self.assertEqual(result,{'success': False,'message': "Unable to fetch today's appointments. Please try again."})


    def test_reschedule_normal_appointment_no_free_slot(self):
        normal = Mock()
        normal.doctor_id = 1
        normal.date = "2026-08-20"
        normal.appointment_id = 10

        self.appointment_s.doc_sched_s.get_doctor_slots.return_value = [("09:00","09:30")]

        self.appointment_s.get_doctors_free_slots = Mock()
        self.appointment_s.get_doctors_free_slots.return_value = ([],"")

        result = self.appointment_s.reschedule_normal_appointment(normal)

        self.assertEqual(result,{'success':False,'message':'No free slot to reschedule appointment.'})


    @patch("services.appointments_service.dblogger")    
    def test_reschedule_normal_appointment_error(self,mocked_dblogger):
        normal = Mock()
        normal.doctor_id = 1
        normal.date = "2026-08-20"
        normal.appointment_id = 10

        self.appointment_s.doc_sched_s.get_doctor_slots.side_effect = sqlite3.Error

        result = self.appointment_s.reschedule_normal_appointment(normal)

        mocked_dblogger.error.assert_called_once()
        self.assertEqual(result,{'success': False,'message': f"Unable to reschedule appointment {normal.appointment_id}. Please try again."})