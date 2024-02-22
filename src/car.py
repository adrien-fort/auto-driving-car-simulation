import re
import logging
from src.display import CarDisplay

# Defining a generic vehicule class first where Car will be a sub-class in case of future enhancement are required
class Vehicle:
    def __init__(self, name, pos_x, pos_y, direction, commands):
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.direction = direction
        self.commands = commands
        self.status = "running"  # currently only "running" or "collided" as expected status but could be extended to idle/parked in future
        self.collision_details = []
    
    def __str__(self):
        return f"{self.name}, ({self.pos_x},{self.pos_y}) {self.direction}, {self.commands}"

    def move_forward(self):
        raise NotImplementedError("Subclasses must implement the move_forward method.")

    def move_backward(self):
        raise NotImplementedError("Subclasses must implement the move_backward method.")

    def turn_left(self):
        raise NotImplementedError("Subclasses must implement the turn_left method.")

    def turn_right(self):
        raise NotImplementedError("Subclasses must implement the turn_right method.")
    
# Defining the Car subclass with methods specific to class (i.e. a future vehicule addition, say motorbike, could have a move_forward method which moves 'faster' +/- 2)
class Car(Vehicle):

    def move(self, dir):
        delta = 1 if dir == "F" else - 1
        if self.direction == 'N':
            self.pos_y = self.pos_y + delta
        elif self.direction == 'S':
            self.pos_y = self.pos_y - delta
        elif self.direction == 'E':
            self.pos_x = self.pos_x + delta
        elif self.direction == 'W':
            self.pos_x = self.pos_x - delta

    def move_forward(self):
        self.move("F")

    def move_backward(self):
        self.move("B")

    def turn_left(self):
        # Define the mapping for left turns and update the car's direction
        turn_left_mapping = {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'}
        self.direction = turn_left_mapping[self.direction]

    def turn_right(self):
        # Define the mapping for right turns and update the car's direction
        turn_right_mapping = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}
        self.direction = turn_right_mapping[self.direction]

# This function simply validates if the input is an Integer, I had to create a separate function as checking directly in the other function caused the tests to fail.
def is_valid_integer(value):
    return value.isdigit()

def car_naming(cars):
    while True:
        try:
            name = input("Please enter the name of the car: ")

            # Check if the name already exists in the cars array and prompt for retry; if the name is unique, break out of the loop and continue with the car creation
            if any(car.name == name for car in cars):
                raise ValueError(f"A car with the name '{name}' already exists. Please choose a different name.\n\n")
            else:
                break
        except ValueError as e:
            print(f"Error: {e} Please try again.")
            logging.warning(f"User input caused the following error: '{e}' and was prompted for retry.")
        
    return name

def car_position(field, cars, name):
    while True:
        try:
            position = input(f"Please enter initial position of car '{name}' in x y Direction format:")

            # Split the input and Check if it has  three parts as expected.
            input_parts = position.split()
            if len(input_parts) != 3:
                raise ValueError("Please enter information in the requested format.")

            # Convert the first two input parts to integers and making direction uppercase
            pos_x, pos_y = map(int, input_parts[:2])
            direction = input_parts[2].upper()

            # Check if both numbers are positive as 
            if pos_x < 0 or pos_y < 0:
                raise ValueError("Please enter positive coordinates.")

            # Validation that position is within the field
            if (pos_x >= field.width or pos_y >= field.height):
                raise ValueError(f'Please enter position within the field of {field.width} x {field.height}, meaning the max numbers are {field.width-1} x {field.height-1} as the field start at 0 x 0.')

            # Validation on the direction, this could be extended in the future to include diagonal directions, i.e. NE
            if direction not in ['N', 'S', 'E', 'W']:
                raise ValueError("Please enter a valid direction!")

            # Validation that no other car already exists at that position
            if any(car.pos_x == pos_x and car.pos_y == pos_y for car in cars):
                raise ValueError("Another car already exists at this position. Please choose a different position.")
            
            break

        except ValueError as e:
            print(f"Error: {e} Please try again.")
            logging.warning(f"User input caused the following error: '{e}' and was prompted for retry.")

    return pos_x, pos_y, direction

def car_commands(name):
    while True:
        try:
            commands = input(f"Please enter the commands for car '{name}':")
            # Define a regular expression pattern allowing only F L R inputs, this could be changed to add idle/parked or even U turn commands
            pattern = re.compile(r'^[FLRB]+$')

            if pattern.match(commands):
                break
            else:
                raise ValueError("Commands invalid, please follow expected format.")
            
        except ValueError as e:
            print(f"Error: {e} Please try again.")
            logging.warning(f"User input caused the following error: '{e}' and was prompted for retry.")
    return commands

def car_creation(field, cars):
    try:
        # Gatherin all inputs and validating them ahead of the car creation
        name = car_naming(cars)

        result_tuple = car_position(field, cars, name)
        pos_x, pos_y, direction = result_tuple

        commands = car_commands(name)
            
        # Creating a new car instance and adding it to the cars array
        new_car = Car(name, pos_x, pos_y, direction, commands)
        cars.append(new_car)
        logging.info(f"User successfully created a new car: {new_car}")

        # Create an instance of CarDisplay
        car_display = CarDisplay()

        # Displaying content of Cars array before exiting
        car_display.pre_sim_display(cars)
        return cars
    except ValueError as e:
            # Handle the error (e.g., print a message)
            print(f"Error: {e} Please try again.")
            logging.warning(f"User input caused the following error: '{e}' and was prompted for retry.")