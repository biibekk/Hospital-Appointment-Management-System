class PatientRepo:
    def __init__(self,connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def patient_exists(self,patientid):
        # query = "select * from patient where id = ?"

        # self.cursor.execute(query,(patientid,))

        # return self.cursor.fetchone()

        return

    def register_patient(self,user):
        query = """Insert into users(name,dob,gender)
        values(?,?,?)"""

        with self.connection:
            self.cursor.execute(query,(user.name,user.dob,user.gender))

        return self.cursor.rowcount