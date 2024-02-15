import pytest
import sys
from unittest.mock import patch
from io import StringIO
from src.car import Car
from src.display import CarDisplay

#Testing the pre sim display function work as expected
def test_car_pre_sim_display(capfd):
    cars = [Car("Car1", 0, 0, 'N', 'F')]
    car_display = CarDisplay()
    car_display.pre_sim_display(cars)
    out, _ = capfd.readouterr()
    assert "Your current list of cars are:" in out
    assert "- Car1, (0, 0) N, F" in out

# Test the output from car post_sim_display function by redirecting standard output to a StringIO object, no collision case
def test_car_post_sim_display_nocol(capsys):
    car1 = Car("Car1", 2, 2, 'N', ['F', 'L', 'F'])
    car2 = Car("Car2", 3, 3, 'S', ['F', 'R', 'F'])
    cars = [car1, car2]

    captured_output = StringIO()
    sys.stdout = captured_output
    try:
        car_display = CarDisplay()
        car_display.post_sim_display(cars)
        captured_output_str = captured_output.getvalue()
        expected_output = "\nAfter simulation, the result is:\n- Car1, (2,2) N\n- Car2, (3,3) S\n"
        assert captured_output_str == expected_output
    finally:
        sys.stdout = sys.__stdout__
