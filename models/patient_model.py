class PatientModel:
    def __init__(self,patient_id,name,dob,gender,contact):
        self.patient_id = patient_id
        self.name = name
        self.dob = dob
        self.gender = gender
        self.contact = contact

    def __str__(self):
        return (
            f"{self.patient_id:<12}"
            f"{self.name:<20}"
            f"{self.dob:<15}"
            f"{self.gender:<12}"
            f"{self.contact:<15}"
        )

    def display_header(self):
        print(
            f"{'Patient ID':<12}"
            f"{'Name':<20}"
            f"{'DOB':<15}"
            f"{'Gender':<12}"
            f"{'Contact':<15}"
        )

        print("-" * 74)
