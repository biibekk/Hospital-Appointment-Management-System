class PatientService:
    def __init__(self,patient_repo_obj):
        self.repo = patient_repo_obj

    def register_patient(self,patient):
        row = self.repo.patient_exists(patient.patient_id)

        if row is None:
            self.repo.register_patient(patient)
            return "added successfully"
        else:
            return "already exists"