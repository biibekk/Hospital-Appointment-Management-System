# python3 -m unittest tests/test_repositories/test_appointments_repo.py
from unittest import TestCase
from unittest.mock import MagicMock

from repositories.appointments_repo import AppointmentsRepo
from models.appointments_model import AppointmentsModel

class TestAppointmentsRepo(TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.appointment = AppointmentsRepo(self.connection)


    def test_get_booked_doctor_slots(self):
        doctor_id = 1
        date = "2026-08-16"
        self.appointment.cursor.fetchall.return_value = [("10:00","10:30"),("11:00","11:30")]

        result = self.appointment.get_booked_doctor_slots(doctor_id, date)

        self.assertEqual(result,[("10:00","10:30"),("11:00","11:30")])
        self.appointment.cursor.execute.assert_called_once_with("""select start_time,end_time from appointments
        where doctor_id = ? and date = ?""",(doctor_id, date))

    def test_check_patient_appointment_overlap_found(self):
        appointment = AppointmentsModel(1,1,2,"2026-08-16","10:00","10:30","BOOKED",2,500,"cold and fever")
        self.appointment.cursor.fetchone.return_value = (1,1,2,"2026-08-16","10:00","10:30","BOOKED",2,500,"cold and fever")
        args = (appointment.patient_id,appointment.date,appointment.end_time,appointment.start_time)

        result = self.appointment.check_patient_appointment_overlap(appointment)

        self.assertIsInstance(result,AppointmentsModel)
        self.appointment.cursor.execute.assert_called_once_with("""select * from appointments
        where patient_id = ? and date = ? and start_time < ? and end_time > ?""",args)

    def test_check_patient_appointment_overlap_not_found(self):
        appointment = AppointmentsModel(1,1,2,"2026-08-16","10:00","10:30","BOOKED",2,500,"cold and fever")
        self.appointment.cursor.fetchone.return_value = None
        args = (appointment.patient_id,appointment.date,appointment.end_time,appointment.start_time)

        result = self.appointment.check_patient_appointment_overlap(appointment)

        self.assertIsNone(result)
        self.appointment.cursor.execute.assert_called_once_with("""select * from appointments
        where patient_id = ? and date = ? and start_time < ? and end_time > ?""",args)


    def test_book_appointment(self):
        appo = AppointmentsModel(None,1,2,"2026-08-16","10:00","10:30","BOOKED",2,500,"cold and fever")  
        self.appointment.cursor.lastrowid = 1

        result = self.appointment.book_appointment(appo)
        args = (appo.patient_id,appo.doctor_id,appo.date,appo.start_time,appo.end_time,appo.status,appo.priority,appo.appointment_cost,
                        appo.problem_description)
        self.assertEqual(result,1)
        self.appointment.cursor.execute.assert_called_once_with("""insert into appointments(patient_id,doctor_id,date,start_time,end_time,status,priority,appointment_cost,problem_description)
        values(?,?,?,?,?,?,?,?,?)""",args)


    def test_cancel_appointment(self):
        appointment_id = 7
        self.appointment.cursor.rowcount = 1

        result = self.appointment.cancel_appointment(appointment_id)

        self.assertEqual(result,1)
        self.appointment.cursor.execute.assert_called_once_with("""delete from appointments
        where appointment_id = ?""",(appointment_id,))


    def test_get_appointment_details_found(self):
        appo = AppointmentsModel(7,1,2,"2026-08-16","10:00","10:30","BOOKED",2,500,"cold and fever")
        self.appointment.cursor.fetchone.return_value = (7,1,2,"2026-08-16","10:00","10:30","BOOKED",2,500,"cold and fever")

        result = self.appointment.get_appointment_details(appo.appointment_id)

        self.assertIsInstance(result, AppointmentsModel)
        self.appointment.cursor.execute.assert_called_once_with("""select * from appointments
        where appointment_id = ?""",(appo.appointment_id,))


    def test_get_appointment_details_not_found(self):
        appointment_id = 7
        self.appointment.cursor.fetchone.return_value = None

        result = self.appointment.get_appointment_details(appointment_id)

        self.assertIsNone(result)
        self.appointment.cursor.execute.assert_called_once_with("""select * from appointments
        where appointment_id = ?""",(appointment_id,))

    def test_reschedule_appointment(self):
        date = "2026-08-17"
        start_time = "11:00"
        end_time = "11:30"
        appointment_id = 7
        self.appointment.cursor.rowcount = 1

        result = self.appointment.reschedule_appointment(date,start_time,end_time,appointment_id)

        self.assertEqual(result,1)
        self.appointment.cursor.execute.assert_called_once_with("""update appointments
        set date = ?, start_time = ?, end_time = ?
        where appointment_id = ?""",(date, start_time, end_time, appointment_id))

    def test_view_appointment_history_found(self):
        patient_id = 1
        rows = [(7,1,2,"2026-08-16","10:00","10:30","BOOKED",2,500,"cold and fever"),
                (8,1,3,"2026-08-17","11:00","11:30","BOOKED",2,600,"chest pain")]
        self.appointment.cursor.fetchall.return_value = rows

        result = self.appointment.view_appointment_history(patient_id)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], AppointmentsModel)
        self.assertIsInstance(result[1], AppointmentsModel)
        self.appointment.cursor.execute.assert_called_once_with("""select * from appointments
        where patient_id = ?""",(patient_id,))

    def test_view_appointment_history_not_found(self):
        patient_id = 1
        self.appointment.cursor.fetchall.return_value = []

        result = self.appointment.view_appointment_history(patient_id)

        self.assertIsNone(result)
        self.appointment.cursor.execute.assert_called_once_with("""select * from appointments
        where patient_id = ?""",(patient_id,))

    def test_get_doctor_appointments_today_found(self):
        doctor_id = 2
        date = "2026-08-16"
        self.appointment.cursor.fetchall.return_value = [(7,1,2,"2026-08-16","10:00","10:30","BOOKED",2,500,"cold and fever")]

        result = self.appointment.get_doctor_appointments_today(doctor_id,date)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result),1)
        self.assertIsInstance(result[0],AppointmentsModel)

        self.appointment.cursor.execute.assert_called_once_with("""select * from appointments
        where doctor_id = ? and date = ?""",(doctor_id,date))

    def test_get_doctor_appointments_today_not_found(self):
        doctor_id = 2
        date = "2026-08-16"
        self.appointment.cursor.fetchall.return_value = []

        result = self.appointment.get_doctor_appointments_today(doctor_id,date)

        self.assertIsNone(result)
        self.appointment.cursor.execute.assert_called_once_with("""select * from appointments
        where doctor_id = ? and date = ?""",(doctor_id, date))

    def test_get_normal_appointment_found(self):
        doctor_id = 2
        date = "2026-08-16"
        start_time = "10:00"
        priority = 2
        self.appointment.cursor.fetchone.return_value = (10,1,2,"2026-08-16","10:00","10:30","BOOKED",2,500,"cold and fever")

        result = self.appointment.get_normal_appointment(doctor_id,date,start_time)

        self.assertIsInstance(result, AppointmentsModel)
        self.appointment.cursor.execute.assert_called_once_with("""select * from appointments
        where doctor_id = ? and date = ? and start_time = ? and priority = ?""",(doctor_id,date,start_time,priority))

    def test_get_normal_appointment_not_found(self):
        doctor_id = 2
        date = "2026-08-16"
        start_time = "10:00"
        priority = 2
        self.appointment.cursor.fetchone.return_value = None

        result = self.appointment.get_normal_appointment(doctor_id,date,start_time)

        self.assertIsNone(result)
        self.appointment.cursor.execute.assert_called_once_with("""select * from appointments
        where doctor_id = ? and date = ? and start_time = ? and priority = ?""",(doctor_id,date,start_time,priority))
