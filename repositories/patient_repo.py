from models.patient_model import PatientModel

class PatientRepo:
    def __init__(self,connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def patient_exists(self,patient):
        # query = "select * from patient where id = ?"

        # self.cursor.execute(query,(patient.patient_id,))

        # return self.cursor.fetchone()

        return False

    def register_patient(self,patient):
        query = """Insert into patient(name,dob,gender,contact)
        values(?,?,?,?)"""

        with self.connection:
            self.cursor.execute(query,(patient.name,patient.dob,patient.gender,patient.contact))

        return self.cursor.rowcount

    def get_patient_info(self,patient_id):
        query = """select * from patient
        where patient_id = ?"""

        with self.connection:
            self.cursor.execute(query,(patient_id,))

        row = self.cursor.fetchone()
        return None if row is None else PatientModel(*row)