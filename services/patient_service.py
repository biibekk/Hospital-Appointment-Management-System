from helpers.display_help import display

class PatientService:
    def __init__(self,patient_repo_obj):
        self.repo = patient_repo_obj

    def register_patient(self,patient):
        row = self.repo.patient_exists(patient)

        if not row:
            res = self.repo.register_patient(patient)
            if(res==1):
                display("Patient Registration Successfully.")
            else:
                display("Patient Registration Failed.")
        else:
            display("Patient Account Already Exists.")