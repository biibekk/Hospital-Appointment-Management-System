# python3 -m unittest tests/test_repositories/test_patient_repo.py
from unittest import TestCase
from unittest.mock import Mock, MagicMock
from repositories.patient_repo import PatientRepo
from models.patient_model import PatientModel

class TestPatient(TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.patient = PatientRepo(self.connection)
        """
        in repo, self.cursor = connection.cursor()   -> mocked method called, return value is another mock by default
        => self.cursor = connection.cursor.return_value (another mock)
        """

    def test_patient_exists_with_id_true(self):
        patient = PatientModel(1, None, None, None, None)
        self.patient.cursor.fetchone.return_value = (1, "Rahul", "2000-01-01", "M", 1234)

        result = self.patient.patient_exists(patient)

        self.assertEqual(result, 1)
        self.patient.cursor.execute.assert_called_once_with("select * from patient where patient_id = ?",(patient.patient_id,))


    def test_patient_exists_with_id_false(self):
        patient = PatientModel(1, "Rahul", "2000-01-01", "M", 1234)
        self.patient.cursor.fetchone.return_value = None

        result = self.patient.patient_exists(patient)

        self.assertIsNone(result)
        self.patient.cursor.execute.assert_called_once_with("select * from patient where patient_id = ?",(patient.patient_id,))


    def test_patient_exists_without_id_true(self):
        patient = PatientModel(None, "Rahul", "2000-01-01", "M", 1234)
        self.patient.cursor.fetchone.return_value = (1, "Rahul", "2000-01-01", "M", 1234)

        result = self.patient.patient_exists(patient)

        self.assertEqual(result, 1)
        self.patient.cursor.execute.assert_called_once_with("select * from patient where name = ? and dob = ? and gender = ? and contact = ?"   ,
            (patient.name,patient.dob,patient.gender,patient.contact))


    def test_patient_exists_without_id_false(self):
        patient = PatientModel(None, "Rahul", "2000-01-01", "male", 1234)
        self.patient.cursor.fetchone.return_value = None

        result = self.patient.patient_exists(patient)

        self.assertIsNone(result)
        self.patient.cursor.execute.assert_called_once_with("select * from patient where name = ? and dob = ? and gender = ? and contact = ?",
        (patient.name, patient.dob, patient.gender, patient.contact))


    def test_register_patient(self):
        self.patient.cursor.lastrowid = 1
        # self.connection.cursor.return_value = a mock => mock.rowcount = 1
        patient = PatientModel(None,"patient1","2004/1/1","male",123)
        
        result = self.patient.register_patient(patient)

        self.assertEqual(result, 1)
        self.patient.cursor.execute.assert_called_once_with("""Insert into patient(name,dob,gender,contact)
        values(?,?,?,?)""",(patient.name,patient.dob,patient.gender,patient.contact))


    def test_get_patient_info_exists(self):
        patient = PatientModel(1,"Rahul","2004-01-01","M",1234)
        self.patient.cursor.fetchone.return_value = (1, "Rahul", "2004-01-01", "M", 1234)

        result = self.patient.get_patient_info(patient.patient_id)

        self.patient.cursor.execute.assert_called_once_with("""select * from patient
        where patient_id = ?""",(patient.patient_id,))
        self.assertIsInstance(result, PatientModel)
        self.assertEqual(result.patient_id, 1)
        self.assertEqual(result.name, "Rahul")
        self.assertEqual(result.dob, "2004-01-01")
        self.assertEqual(result.gender, "M")
        self.assertEqual(result.contact, 1234)


    def test_get_patient_info_none(self):
        patient_id = 1
        self.patient.cursor.fetchone.return_value = None

        result = self.patient.get_patient_info(patient_id)

        self.patient.cursor.execute.assert_called_once_with("""select * from patient
        where patient_id = ?""",(patient_id,))
        self.assertIsNone(result)