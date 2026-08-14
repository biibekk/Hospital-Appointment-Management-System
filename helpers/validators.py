from datetime import datetime
import re

from helpers.display_help import display

class Validators:
    def get_int(prompt, error_message = "Invalid input! Please enter a whole number."):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                display(f"Error: {error_message}")

    def get_choice(prompt,min_val,max_val):
        while True:
            value = Validators.get_int(prompt)

            if min_val <= value <= max_val:
                return value

            display(f"Error: Please enter a number between {min_val} and {max_val}.")

    def get_choice_from_list(prompt,list_options,field_name):
         while True:
            try:
                doctor_input = int(input(prompt))

                if doctor_input in list_options:
                    return doctor_input
                else:
                    display(f"Error: Please enter {field_name} ID from above options: ")

            except ValueError:
                display("Error: Invalid input! Please enter a whole number")

    def get_future_date(prompt):
        while True:
            date_input = input(prompt).strip()
            try:
                # Validates format AND checks if date exists on calendar
                # string -> datetime -> date
                selected_date = datetime.strptime(date_input,"%Y-%m-%d").date()

                if selected_date < datetime.now().date():
                    display("Error: Date cannot be in the past.")
                    continue
                return selected_date.strftime("%Y-%m-%d")
            except ValueError:
                display("Error: Invalid date format or non-existent date! Please use YYYY-MM-DD.")

    def get_past_date(prompt):
            while True:
                date_input = input(prompt).strip()
                try:
                    # Validates format AND checks if date exists on calendar
                    # string -> datetime -> date
                    selected_date = datetime.strptime(date_input,"%Y-%m-%d").date()
    
                    if selected_date > datetime.now().date():
                        display("Error: Date cannot be in the future.")
                        continue
                    return selected_date.strftime("%Y-%m-%d")
                except ValueError:
                    display("Error: Invalid date format or non-existent date! Please use YYYY-MM-DD.")

    def get_non_empty_string(prompt):
        while True:
            value = input(prompt).strip()

            if not value:
                display("Error: Input cannot be empty.")
                continue

            return value

    def get_problem_description(prompt):
        while True:
            value = input(prompt).strip()

            if not value:
                display("Error: Description cannot be empty.")
                continue

            if len(value) <= 10:
                display("Error: Description must be longer than 10 characters.")
                continue

            if value.isdigit():
                display("Error: Description cannot contain digits only.")
                continue

            return value

    def get_single_charater(prompt,chars):
        while True:
            value = input(prompt).strip()

            if not value:
                display("Error: Input cannot be empty.")
                continue

            if len(value) != 1:
                display(f"Error: Gender must be 1 character{chars} only.")
                continue

            value = value.upper()
            if value not in chars:
                display(f"Error: Gender must be valid character{chars} only.")
                continue

            return value
        
    def get_contact(prompt,length):
        while True:
            value = input(prompt).strip()
            if not value:
                display("Error: Contact cannot be empty.")
                continue

            if not value.isdigit():
                display(f"Error: Contact must be {length} digits only.")
                continue

            if len(value) != length:
                display(f"Error: Contact must be exactly {length} digits only.")
                continue
            return value

    def get_time(prompt):
        while True:
            value = input(prompt)
            if not re.fullmatch(r"\d{2}:\d{2}", value):
                display("Please enter time as HH:MM, e.g. 01:00 or 13:00")
                continue

            try:
                time_obj = datetime.strptime(value,"%H:%M").time()
                return time_obj.strftime("%H:%M")

            except ValueError:
                display("Invalid time. Please use valid 24-hour(HH:MM) time.")