# python3 -m unittest tests/test_repositories/test_doctor_repo.py
import sqlite3
from unittest import TestCase
from unittest.mock import MagicMock
from repositories.doctor_repo import DoctorRepo
from models.doctor_model import DoctorModel

class TestDoctorRepo(TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.doctor = DoctorRepo(self.connection)
        # self.connection.cursor() - >self.connection.cursor.return_value

    def test_doctor_exists_with_id_true(self):
        doctor = DoctorModel(1,None,None,None,None)
        self.doctor.cursor.fetchone.return_value = (1,"demo",1234,"surgeon",1000)

        result = self.doctor.doctor_exists(doctor)
        # expected = DoctorModel(1,"demo",1234,"surgeon",1000)

        self.assertIsInstance(result, DoctorModel)
        # self.assertEqual(result,expected)   # checks result is expected (need __eq__() method for that)
        self.assertEqual(result.doctor_id, 1)
        self.assertEqual(result.name, "demo")
        self.assertEqual(result.contact, 1234)
        self.assertEqual(result.specialisation, "surgeon")
        self.assertEqual(result.consultation_fee, 1000)
        self.doctor.cursor.execute.assert_called_once()
        self.doctor.cursor.execute.assert_called_once_with("select * from doctor where doctor_id = ?",(doctor.doctor_id,))

    def test_doctor_exists_with_id_false(self):
            doctor = DoctorModel(1,"demo",1234,"physician",100)
            self.doctor.cursor.fetchone.return_value = None
    
            result = self.doctor.doctor_exists(doctor)
    
            self.assertEqual(result,None)
            self.doctor.cursor.execute.assert_called_once()
            self.doctor.cursor.execute.assert_called_once_with("select * from doctor where doctor_id = ?",(doctor.doctor_id,))

    def test_doctor_exists_without_id_true(self):
        doc = DoctorModel(None,"demo",1234,"physician",100)
        self.doctor.cursor.fetchone.return_value = (1,"demo",1234,"surgeon",1000)

        result = self.doctor.doctor_exists(doc)

        self.assertIsInstance(result,DoctorModel)
        self.assertEqual(result.doctor_id, 1)
        self.assertEqual(result.name, "demo")
        self.assertEqual(result.contact, 1234)
        self.assertEqual(result.specialisation, "surgeon")
        self.assertEqual(result.consultation_fee, 1000)
        self.doctor.cursor.execute.assert_called_once()
        self.doctor.cursor.execute.assert_called_once_with('select * from doctor where name = ? and contact = ?', ('demo', 1234))

    def test_doctor_exists_without_id_false(self):
            doc = DoctorModel(None,"demo",1234,"physician",100)
            self.doctor.cursor.fetchone.return_value = None

            result = self.doctor.doctor_exists(doc)
    
            self.assertEqual(result,None)  
    
            self.doctor.cursor.execute.assert_called_once()
            self.doctor.cursor.execute.assert_called_once_with('select * from doctor where name = ? and contact = ?', ('demo', 1234))

    def test_add_doctor(self):
        doctor = DoctorModel(None,"demo",1234,"physician",100)
        self.doctor.cursor.rowcount = 1

        result = self.doctor.add_doctor(doctor)

        self.assertEqual(result,1)
        self.doctor.cursor.execute.assert_called_once()
        self.doctor.cursor.execute.assert_called_once_with("""insert into doctor(name,contact,specialisation,consultation_fee) 
        values(?,?,?,?)""",(doctor.name,doctor.contact,doctor.specialisation,doctor.consultation_fee))

