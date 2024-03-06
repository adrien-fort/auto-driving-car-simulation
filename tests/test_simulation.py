from io import StringIO
import sys
import pytest
from unittest.mock import patch, MagicMock
from src.simulation import Simulation, CarSimulation, run_simulation
from src.car import Car
from src.field import Field

@pytest.fixture
def field():
    class DummyField:
        width = 5
        height = 5
    return DummyField()

# Testing the function that confirms if two cars have collided
def test_is_car_collision():
    car1 = Car("Car1", 0, 0, 'N', [])
    car2 = Car("Car2", 0, 1, 'N', [])
    car3 = Car("Car3", 2, 2, 'S', [])
    cars = [car1, car2, car3]

    car_simulation = CarSimulation()
    assert car_simulation.is_car_collision(cars, car1, 0, 1)
    assert car_simulation.is_car_collision(cars, car1, 2, 2)

# Testing the function that goes to fetch the collided car name
def test_get_collided_car_name():
    car1 = Car("Car1", 0, 0, 'N', [])
    car2 = Car("Car2", 0, 0, 'N', [])
    car3 = Car("Car3", 2, 2, 'S', [])
    cars = [car1, car2, car3]

    car_simulation = CarSimulation()
    assert car_simulation.get_collided_car_name(cars, car1) == "Car2"
    assert car_simulation.get_collided_car_name(cars, car2) == "Car1"
    assert car_simulation.get_collided_car_name(cars, car3) is None

# Testing the function which updates the collided car status and collision details
def test_update_collided_cars():
    car1 = Car("Car1", 2, 3, 'N', [])
    car2 = Car("Car2", 2, 3, 'S', [])
    car3 = Car("Car3", 2, 3, 'W', [])
    cars = [car1, car2, car3]

    car_simulation = CarSimulation()
    car_simulation.update_collided_cars(cars, car2, 0)

    assert car2.status == "collided"
    assert car2.collision_details == [{'with_car': 'Car1', 'step': 0},{'with_car': 'Car3', 'step': 0}]

    car_simulation.update_collided_cars(cars, car3, 0)

    assert car3.status == "collided"
    assert car3.collision_details == [{'with_car': 'Car2', 'step': 0},{'with_car': 'Car1', 'step': 0}]

# Testing the function which ensures car is still in boundary of the field
def test_is_within_boundaries(field):
    simulation = Simulation()
    assert simulation.is_within_boundaries(field, 2, 3)
    assert not simulation.is_within_boundaries(field, 6, 3)

# Testing the execute command which orchestrate all the checks and actions by forcing a collision with car2
def test_execute_command(capsys):
    car = Car("Car1", 2, 2, 'N', ['F', 'L', 'F'])
    car2 = Car("Car2", 1, 3, 'N', ['R', 'L', 'R'])
    cars = [car,car2]
    field = Field(10, 10)

    captured_output = StringIO()
    sys.stdout = captured_output

    car_simulation = CarSimulation()
    car_simulation.execute_car_command(field, car, 'F', cars, 0)
    assert car.pos_y == 3
    assert car.status == "running"
    
    car_simulation.execute_car_command(field, car, 'L', cars, 1)
    assert car.direction == 'W'
    assert car.status == "running"

    car_simulation.execute_car_command(field, car, 'F', cars, 2)
    assert car.status == "collided"

# Testing an end to end run of the simulation with two cars and a dummy field, no collision case
def test_run_simul_nocol(capsys):
    car1 = Car("Car1", 2, 2, 'N', ['F', 'L', 'F'])
    car2 = Car("Car2", 3, 3, 'S', ['F', 'R', 'F'])
    cars = [car1, car2]
    field = Field(10, 10)

    captured_output = StringIO()
    sys.stdout = captured_output
    try:
        run_simulation(field, cars)
        captured_output_str = captured_output.getvalue()
        expected_output = "\nYour current list of cars are:\n- Car1, (2, 2) N, ['F', 'L', 'F']\n- Car2, (3, 3) S, ['F', 'R', 'F']\n\nAfter simulation, the result is:\n- Car1, (1,3) W\n- Car2, (2,2) W\n"
        assert captured_output_str == expected_output
    finally:
        sys.stdout = sys.__stdout__

# Testing an end to end run of the simulation with two cars and a dummy field, collision case
def test_run_simul_col(capsys):
    car1 = Car("Car1", 2, 3, 'E', ['F', 'F', 'R'])
    car2 = Car("Car2", 4, 3, 'W', ['F', 'F', 'L'])
    cars = [car1, car2]
    field = Field(10, 10)

    captured_output = StringIO()
    sys.stdout = captured_output
    try:
        run_simulation(field, cars)
        captured_output_str = captured_output.getvalue()
        expected_output = "\nYour current list of cars are:\n- Car1, (2, 3) E, ['F', 'F', 'R']\n- Car2, (4, 3) W, ['F', 'F', 'L']\n\nAfter simulation, the result is:\n- Car1, collides with Car2 at (3,3) at step 1\n- Car2, collides with Car1 at (3,3) at step 1\n"
        assert captured_output_str == expected_output
    finally:
        sys.stdout = sys.__stdout__

class MockCar:
    def __init__(self, name, direction, pos_x, pos_y, status="running"):
        self.name = name
        self.direction = direction
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.status = status
        self.collision_details = []

    def move_forward(self):
        # Mock move_forward method
        pass

    def turn_left(self):
        # Mock turn_left method
        pass

    def turn_right(self):
        # Mock turn_right method
        pass

class MockCar:
    def __init__(self, name, direction, pos_x, pos_y, status="running"):
        self.name = name
        self.direction = direction
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.status = status
        self.collision_details = []

    def move_forward(self):
        if self.direction == 'N':
            self.pos_y = self.pos_y + 1
        elif self.direction == 'S':
            self.pos_y = self.pos_y - 1
        elif self.direction == 'E':
            self.pos_x = self.pos_x + 1
        elif self.direction == 'W':
            self.pos_x = self.pos_x - 1

    def move_backward(self):
        if self.direction == 'N':
            self.pos_y = self.pos_y - 1
        elif self.direction == 'S':
            self.pos_y = self.pos_y + 1
        elif self.direction == 'E':
            self.pos_x = self.pos_x - 1
        elif self.direction == 'W':
            self.pos_x = self.pos_x + 1

    def turn_left(self):
        # Mock turn_left method
        pass

    def turn_right(self):
        # Mock turn_right method
        pass

def test_execute_car_command_move_forward_success():
    field = Field(10,10)
    car = MockCar(name="Car1", direction="N", pos_x=3, pos_y=3)
    cars = [car]
    step_counter = 1

    car_simulation = CarSimulation()
    with patch.object(car, 'move_forward') as mock_move_forward:
        car_simulation.execute_car_command(field, car, 'F', cars, step_counter)

    mock_move_forward.assert_called_once()

def test_execute_car_command_move_backward_success():
    field = Field(10,10)
    car = MockCar(name="Car1", direction="N", pos_x=3, pos_y=3)
    cars = [car]
    step_counter = 1

    car_simulation = CarSimulation()
    with patch.object(car, 'move_backward') as mock_move_backward:
        car_simulation.execute_car_command(field, car, 'B', cars, step_counter)

    mock_move_backward.assert_called_once()

def test_execute_car_command_turn_left():
    field = Field(10,10)
    car = MockCar(name="Car1", direction="N", pos_x=3, pos_y=3)
    cars = [car]
    step_counter = 1

    car_simulation = CarSimulation()
    with patch.object(car, 'turn_left') as mock_turn_left:
        car_simulation.execute_car_command(field, car, 'L', cars, step_counter)

    mock_turn_left.assert_called_once()