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

    def test_register_patient(self):
        self.patient.cursor.lastrowid = 1
        # self.connection.cursor.return_value = a mock => mock.rowcount = 1
        patient = PatientModel(None,"patient1","2004/1/1","male",123)
        
        result = self.patient.register_patient(patient)

        self.assertEqual(result, 1)
        self.patient.cursor.execute.assert_called_once_with("""Insert into patient(name,dob,gender,contact)
        values(?,?,?,?)""",(patient.name,patient.dob,patient.gender,patient.contact))