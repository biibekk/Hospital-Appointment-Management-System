class DoctorRepo:
    def __init__(self,connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def doctor_exists(self,doctor):
        query = "select * from doctor where doctor_id = ?"
        args = (doctor.doctor_id,)

        if doctor.doctor_id is None:
            query = "select * from doctor where name = ? and contact = ?"
            args = (doctor.name,doctor.contact)

        self.cursor.execute(query,args)

        return self.cursor.fetchone()

    def add_doctor(self,doctor):
        query = """insert into doctor(name,contact,specialisation,consultation_fee) 
        values(?,?,?,?)"""

        with self.connection:
            self.cursor.execute(query,(doctor.name,doctor.contact,doctor.specialisation,doctor.consultation_fee))

        return self.cursor.rowcount