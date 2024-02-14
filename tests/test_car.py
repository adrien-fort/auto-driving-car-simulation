import pytest
from unittest.mock import patch
from io import StringIO
from src.car import Vehicle, Car, car_creation, car_position, car_naming, car_commands
from src.display import CarDisplay


# Mocking input function
def simulate_user_input(inputs):
    return lambda _: inputs.pop(0) if inputs else "default_input"

#Testing the overall vehicule class
def test_vehicle_creation():
    vehicle = Vehicle("TestVehicle", 0, 0, 'N', 'F')
    assert vehicle.name == "TestVehicle"
    assert vehicle.pos_x == 0
    assert vehicle.pos_y == 0
    assert vehicle.direction == 'N'
    assert vehicle.commands == 'F'
    assert vehicle.status == "running"
    assert vehicle.collision_details == []

#Testing the Car subclass behaves as expected
def test_car_creation():
    car = Car("TestCar", 1, 2, 'S', 'FRFL')
    assert car.name == "TestCar"
    assert car.pos_x == 1
    assert car.pos_y == 2
    assert car.direction == 'S'
    assert car.commands == 'FRFL'
    assert car.status == "running"
    assert car.collision_details == []

# Testing the move forward method from the vehicule parent class (this method is to be defined in subclass)
def test_vehicle_move_forward():
    vehicle = Vehicle("TestVehicle", 0, 0, 'N', 'F')
    with pytest.raises(NotImplementedError):
        vehicle.move_forward()

# Testing the move backward method from the vehicule parent class (this method is to be defined in subclass)
def test_vehicle_move_backward():
    vehicle = Vehicle("TestVehicle", 0, 0, 'N', 'B')
    with pytest.raises(NotImplementedError):
        vehicle.move_backward()

# Testing the move forward method from the car subclass
def test_car_move_forward():
    car = Car("TestCar", 1, 2, 'S', 'FRFL')
    car.move_forward()
    assert car.pos_x == 1
    assert car.pos_y == 1

# Testing the move Backward method from the car subclass
def test_car_move_backward():
    car = Car("TestCar", 1, 2, 'S', 'B')
    car.move_backward()
    assert car.pos_x == 1
    assert car.pos_y == 3

# Testing the turn left method from vehicul parent class (this method is to be defined in subclass)
def test_vehicle_turn_left():
    vehicle = Vehicle("TestVehicle", 0, 0, 'N', 'F')
    with pytest.raises(NotImplementedError):
        vehicle.turn_left()

# Testing the turn left method from car subclass
def test_car_turn_left():
    car = Car("TestCar", 1, 2, 'S', 'FRFL')
    car.turn_left()
    assert car.direction == 'E'

# Testing the turn right method from vehicul parent class (this method is to be defined in subclass)
def test_vehicle_turn_right():
    vehicle = Vehicle("TestVehicle", 0, 0, 'N', 'F')
    with pytest.raises(NotImplementedError):
        vehicle.turn_right()

# Testing the turn right method from car subclass
def test_car_turn_right():
    car = Car("TestCar", 1, 2, 'S', 'FRFL')
    car.turn_right()
    assert car.direction == 'W'

# Testing input validation for 2 cars in same place by using a dummy field
def test_car_creation_input_validation(capfd):
    class DummyField:
        width = 10
        height = 10
    cars = [Car("Car1", 0, 0, 'N', 'F')]
    with pytest.raises(StopIteration):
        with patch('builtins.input', side_effect=["Car2", "0 0 N", "F"]):
            car_creation(DummyField, cars)
    out, _ = capfd.readouterr()
    assert "Error: Another car already exists at this position. Please choose a different position. Please try again." in out

#Testing the main car_creation function
def test_car_creation_with_commands():
    # Create a dummy field object with a width and height
    class DummyField:
        width = 10
        height = 10

    cars = []

    # Mock user input for car creation
    user_input = ["Car1", "2 2 N", "FFLFFLFF"]

    with patch('builtins.input', side_effect=user_input):
        result = car_creation(DummyField, cars)

    # Check the resulting cars list
    assert len(result) == 1
    car = result[0]
    assert car.name == "Car1"
    assert car.pos_x == 2
    assert car.pos_y == 2
    assert car.direction == 'N'
    assert car.commands == "FFLFFLFF"

    # Display the cars to see the result
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        CarDisplay.pre_sim_display(result)
        output = mock_stdout.getvalue()

    # Check if the display output is as expected
    assert "- Car1, (2, 2) N, FFLFFLFF" in output

def test_car_position_valid_input():
    class DummyField:
        width = 10
        height = 10
    cars = []

    with patch("builtins.input", side_effect=["5 5 N"]):
        pos_x, pos_y, direction = car_position(DummyField, cars, "Car1")

    assert pos_x == 5
    assert pos_y == 5
    assert direction == "N"

def test_car_naming_unique_name():
    cars = []  # An empty list to simulate no existing cars

    with patch("builtins.input", return_value="Car1"):
        result = car_naming(cars)

    assert result == "Car1"


def test_car_commands_valid_input():
    name = "Car1"  # Replace with the desired car name
    valid_commands = "FFLFRF"

    with patch("builtins.input", return_value=valid_commands):
        result = car_commands(name)

    assert result == valid_commands

def test_car_commands_invalid_input():
    name = "Car2"  # Replace with the desired car name
    invalid_commands = "ABC123"

    with patch("builtins.input", side_effect=[invalid_commands, "FFR"]):
        result = car_commands(name)

    assert result == "FFR"  # The second attempt is a valid input

def test_car_commands_empty_input():
    name = "Car3"  # Replace with the desired car name

    with patch("builtins.input", side_effect=["", "FFL"]):
        result = car_commands(name)

    assert result == "FFL"  # The second attempt is a valid input