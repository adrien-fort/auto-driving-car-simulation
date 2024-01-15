import logging

class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def field_creation():
        while True:
            try:
                # Get input from the user
                user_input = input("Please enter the width and height of the simulation field in x y format:\n")
                
                # Split the input into two parts
                input_parts = user_input.split()

                # Check if two integers are provided
                if len(input_parts) != 2:
                    raise ValueError("Please enter exactly two integers.")

                # Convert the input parts to integers
                width = int(input_parts[0])
                height = int(input_parts[1])

                # Check if both numbers are positive, assuming a field without width or heights isn't allowed
                if width <= 0 or height <= 0:
                    raise ValueError("Please enter positive integers.")

                # If the conversion is successful, give a confirmation and break out of the loop
                print(f"You have created a field of {width} x {height}.")
                logging.info(f"User has created a field of {width} x {height}.")
                break

            except ValueError as e:
                # Handle the error (e.g., invalid input)
                print(f"Error: {e}. Please try again.")
                logging.warning(f"User input caused the following error: '{e}' and was prompted for retry.")

        return Field(width, height)