from datetime import datetime

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

    def get_date(prompt):
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