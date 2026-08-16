class DoctorScheduleModel:
    def __init__(self,schedule_id,doctor_id,date,start_time,end_time,slot_duration=30):
        self.schedule_id = schedule_id
        self.doctor_id = doctor_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.slot_duration = slot_duration

    def __str__(self):
        return f"<DoctorSchedule id='{self.schedule_id}' doctorId='{self.doctor_id}'>"