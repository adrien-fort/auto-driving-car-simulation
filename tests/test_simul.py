from io import StringIO
import sys
import pytest
from src.simul import is_collision, get_collided_car_name, update_collided_cars, is_within_boundaries, execute_command, run_simul
from src.car import Car
from src.field import Field

@pytest.fixture
def field():
    class DummyField:
        width = 5
        height = 5
    return DummyField()

# Testing the function that confirms if two cars have collided
def test_is_collision():
    car1 = Car("Car1", 0, 0, 'N', [])
    car2 = Car("Car2", 0, 1, 'N', [])
    car3 = Car("Car3", 2, 2, 'S', [])
    cars = [car1, car2, car3]

    assert is_collision(cars, car1, 0, 1)
    assert is_collision(cars, car1, 2, 2)

# Testing the function that goes to fetch the collided car name
def test_get_collided_car_name():
    car1 = Car("Car1", 0, 0, 'N', [])
    car2 = Car("Car2", 0, 0, 'N', [])
    car3 = Car("Car3", 2, 2, 'S', [])
    cars = [car1, car2, car3]

    assert get_collided_car_name(cars, car1) == "Car2"
    assert get_collided_car_name(cars, car2) == "Car1"
    assert get_collided_car_name(cars, car3) is None

# Testing the function which updates the collided car status and collision details
def test_update_collided_cars():
    car1 = Car("Car1", 0, 0, 'N', [])
    car2 = Car("Car2", 0, 0, 'N', [])
    car3 = Car("Car3", 2, 2, 'S', [])
    car4 = Car("Car4", 2, 2, 'S', [])
    cars = [car1, car2, car3, car4]

    update_collided_cars(cars, car1)

    assert car2.status == "collided"
    assert car2.collision_details == [{'with_car': 'Car1', 'step': 0}]

    update_collided_cars(cars, car3)

    assert car4.status == "collided"
    assert car4.collision_details == [{'with_car': 'Car3', 'step': 0}]

# Testing the function which ensures car is still in boundary of the field
def test_is_within_boundaries(field):
    assert is_within_boundaries(field, 2, 3)
    assert not is_within_boundaries(field, 6, 3)

# Testing the execute command which orchestrate all the checks and actions by forcing a collision with car2
def test_execute_command(capsys):
    car = Car("Car1", 2, 2, 'N', ['F', 'L', 'F'])
    car2 = Car("Car2", 1, 3, 'N', ['R', 'L', 'R'])
    cars = [car,car2]
    field = Field(10, 10)

    captured_output = StringIO()
    sys.stdout = captured_output

    execute_command(field, car, 'F', cars, 0)
    assert car.pos_y == 3
    assert car.status == "running"
    
    execute_command(field, car, 'L', cars, 1)
    assert car.direction == 'W'
    assert car.status == "running"

    execute_command(field, car, 'F', cars, 2)
    assert car.status == "collided"

# Testing an end to end run of the simulation with two cars and a dummy field, no collision case
def test_run_simul(capsys):
    car1 = Car("Car1", 2, 2, 'N', ['F', 'L', 'F'])
    car2 = Car("Car2", 3, 3, 'S', ['F', 'R', 'F'])
    cars = [car1, car2]
    field = Field(10, 10)

    captured_output = StringIO()
    sys.stdout = captured_output
    try:
        run_simul(field, cars)
        captured_output_str = captured_output.getvalue()
        expected_output = "\nYour current list of cars are:\n- Car1, (2, 2) N, ['F', 'L', 'F']\n- Car2, (3, 3) S, ['F', 'R', 'F']\n\nAfter simulation, the result is:\n- Car1, (1,3) W\n- Car2, (2,2) W\n"
        assert captured_output_str == expected_output
    finally:
        sys.stdout = sys.__stdout__

# Testing an end to end run of the simulation with two cars and a dummy field, collision case
def test_run_simul(capsys):
    car1 = Car("Car1", 2, 3, 'E', ['F', 'F', 'R'])
    car2 = Car("Car2", 4, 3, 'W', ['F', 'F', 'L'])
    cars = [car1, car2]
    field = Field(10, 10)

    captured_output = StringIO()
    sys.stdout = captured_output
    try:
        run_simul(field, cars)
        captured_output_str = captured_output.getvalue()
        expected_output = "\nYour current list of cars are:\n- Car1, (2, 3) E, ['F', 'F', 'R']\n- Car2, (4, 3) W, ['F', 'F', 'L']\n\nAfter simulation, the result is:\n- Car1, collides with Car2 at (3,3) at step 1\n- Car2, collides with Car1 at (3,3) at step 1\n"
        assert captured_output_str == expected_output
    finally:
        sys.stdout = sys.__stdout__