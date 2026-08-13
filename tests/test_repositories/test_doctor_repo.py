from unittest import TestCase
from unittest.mock import MagicMock
from repositories.doctor_repo import DoctorRepo
from models.doctor_model import DoctorModel

class TestDoctorRepo(TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.doctor = DoctorRepo(self.connection)

    def test_doctor_exists_true(self):
        doc = DoctorModel("demo",1234,"physician",100,1)

        self.connection.cursor.return_value.fetchone.return_value = 1
        result = self.doctor.doctor_exists(doc)

        self.assertEqual(result,1)

        self.connection.cursor.return_value.execute.assert_called_once()

    def test_doctor_exists_false(self):
        doc = DoctorModel("demo",1234,"physician",100)

        # self.connection.cursor.return_value.fetchone.return_value = 0
        # self.connection.cursor is mocked method and its return_value is store in self.doctor.cursor in repo
        self.doctor.cursor.fetchone.return_value = 0
        result = self.doctor.doctor_exists(doc)

        self.assertEqual(result,0)  

        # self.connection.cursor
        self.doctor.cursor.execute.assert_called_once()
        self.doctor.cursor.execute.assert_called_once_with()

