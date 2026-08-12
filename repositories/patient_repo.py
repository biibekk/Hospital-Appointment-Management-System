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