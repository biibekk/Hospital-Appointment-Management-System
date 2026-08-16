from models.patient_model import PatientModel

class PatientRepo:
    def __init__(self,connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def patient_exists(self,patient):
        query = "select * from patient where id = ?"
        args = (patient.patient_id,)

        if patient.patient_id is None:
            query = "select * from patient where name = ? and dob = ? and gender = ? and contact = ?"
            args = (patient.name,patient.dob,patient.gender,patient.contact)

        self.cursor.execute(query,args)

        row =  self.cursor.fetchone()
        return None if row is None else row[0]

    def register_patient(self,patient):
        query = """Insert into patient(name,dob,gender,contact)
        values(?,?,?,?)"""

        with self.connection:
            self.cursor.execute(query,(patient.name,patient.dob,patient.gender,patient.contact))

        return self.cursor.lastrowid

    def get_patient_info(self,patient_id):
        query = """select * from patient
        where patient_id = ?"""

        with self.connection:
            self.cursor.execute(query,(patient_id,))

        row = self.cursor.fetchone()
        return None if row is None else PatientModel(*row)