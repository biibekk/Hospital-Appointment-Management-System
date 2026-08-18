# python3 -m unittest tests/test_repositories/test_doctorschedule_repo.py 
from unittest import TestCase
from unittest.mock import MagicMock

from repositories.doctorschedule_repo import DoctorScheduleRepo
from models.doctorschedule_model import DoctorScheduleModel

class TestDoctorScheduleRepo(TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.doc_sched = DoctorScheduleRepo(self.connection)

    def test_doctor_schedule_exists(self):
        schedule = DoctorScheduleModel(1,2,"2026-08-15","10:00","14:00",30)
        self.doc_sched.cursor.fetchone.return_value = True
        args = (schedule.doctor_id,schedule.date,schedule.end_time,schedule.start_time)

        result = self.doc_sched.doctor_schedule_exists(schedule)

        self.doc_sched.cursor.execute.assert_called_once_with("""select 1 from doctorschedule
        where doctor_id = ? and date = ? and start_time < ? and end_time > ?""",args)
        self.assertEqual(result,True)

    def test_doctor_schedule_exists_false(self):
        schedule = DoctorScheduleModel(1,2,"2026-08-20","10:00","10:30")
        self.doc_sched.cursor.fetchone.return_value = None

        result = self.doc_sched.doctor_schedule_exists(schedule)

        self.assertEqual(result,False)

    def test_add_doctor_schedule(self):
        schedule = DoctorScheduleModel(1,2,"2026-08-15","10:00","14:00",30)
        self.doc_sched.cursor.rowcount = 1

        result = self.doc_sched.add_doctor_schedule(schedule)

        self.doc_sched.cursor.execute.assert_called_once_with("""insert into doctorschedule(doctor_id,date,start_time,end_time,slot_duration)
        values(?, ?, ?, ?, ?)""",(schedule.doctor_id,schedule.date,schedule.start_time,schedule.end_time,schedule.slot_duration))
        self.assertEqual(result,1)

    def test_get_doctor_slots(self):
        doctor_id = 1
        date = "2026-08-15"
        self.doc_sched.cursor.fetchall.return_value = [(1,"10:00","13:00",30),(2,"09:00","14:00",30)]

        result = self.doc_sched.get_doctor_slots(doctor_id,date)

        self.doc_sched.cursor.execute.assert_called_once_with("""select schedule_id,start_time,end_time,slot_duration from doctorschedule 
        where doctor_id = ? and date = ?""",(doctor_id,date))
        self.assertEqual(result,[(1,"10:00","13:00",30),(2,"09:00","14:00",30)])
