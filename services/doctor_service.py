from helpers.display_help import display

class DoctorService:
    def __init__(self,doctor_repo):
        self.repo = doctor_repo

    def add_doctor(self,doctor):
        if self.repo.doctor_exists(doctor):
            display("Doctor Already Exists")
            return

        res = self.repo.add_doctor(doctor)
        if(res==1):
            display("Doctor Added Successfully.")
        else:
            display("Failed to Add Doctor.")