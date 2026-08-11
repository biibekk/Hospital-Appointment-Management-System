class DoctorModel:
    def __init__(self,doctor_id,name,specialisation,fee):
        self.doctor_id = doctor_id
        self.name = name
        self.specialisation = specialisation
        self.consultation_fee = fee

    def __str__(self):
        return f"<Doctor name='{self.name}' id='{self.doctor_id}'>"