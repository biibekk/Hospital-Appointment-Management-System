class PatientModel:
    def __init__(self,name,dob,gender,contact,patient_id=None):
        self.patient_id = patient_id
        self.name = name
        self.dob = dob
        self.gender = gender
        self.contact = contact

    def __str__(self):
        return f"<Patient name='{self.name} id='{self.id}'>"