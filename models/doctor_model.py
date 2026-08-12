class DoctorModel:
    def __init__(self,name,contact,specialisation,fee,doctor_id=None):
        self.doctor_id = doctor_id
        self.name = name
        self.contact = contact
        self.specialisation = specialisation
        self.consultation_fee = fee

    def __str__(self):
        return f"<Doctor name='{self.name}' id='{self.doctor_id}'>"