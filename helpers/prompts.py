class Prompts:
    menu_prompt = f"""\n{'-'*37}
     Hospital Appointment System
{'-'*37}
1. Hospital Admin
2. Doctor
3. Patient
4. Quit
Enter your choice: """


    patient_menu = f"""\n{'-'*23}
     Patient Menu
{'-'*23}
1. Register Patient
2. Book Appointment
3. Cancel Appointment
4. Reschedule Appointment
5. Get Appointment Status
6. View Appointment History
7. Go Back
Enter your choice: """
    

    patient_id = f"""{'-'*20}
     Patient ID
{'-'*20}
Enter Patient ID no: """


    doctor = """\n---------------------
     Select Doctor
----------------------

Doctor Id       Name                     Consultation Fee
{doctors}

Enter Doctor Id: """


    date = f"""\n{'-'*31}
     Select Appointment Date
{'-'*31}
Enter date(yyyy-mm-dd): """


    slot = """\n---------------------
     Select Slot
---------------------

S.No.  Start Time   End Time
{slots}

Enter Slot No: """


    priority = f"""\n{'-'*24}
     Select Priority
{'-'*24}
1. Emergency
2. Normal
Enter your choice: """


    problem_description = f"""\n{'-'*28}
     Problem Description
{'-'*28}
Describe your problem in few words: """